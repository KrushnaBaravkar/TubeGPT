"""
indexing.py
-----------
Stage 1 of the RAG pipeline.

Responsibilities:
  - Accept a YouTube URL (or bare video ID)
  - Fetch the transcript via YouTubeTranscriptApi
  - Split transcript into overlapping chunks
  - Embed chunks with OpenAI embeddings
  - Store embeddings in a FAISS vector store
  - Return everything the retrieval stage needs

Usage:
    from pipeline.indexing import index_video

    result = index_video("https://www.youtube.com/watch?v=fNk_zzaMoSs")
    # or bare ID:
    result = index_video("fNk_zzaMoSs")

    # What you get back:
    result["vector_store"]   # FAISS index  → pass to retrieval.py
    result["chunks"]         # List[Document] → optional, for inspection
    result["transcript"]     # Raw transcript string → optional
    result["video_id"]       # Cleaned video ID
"""

import re
from typing import Union

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


# ── Configuration ────────────────────────────────────────────────────────────

CHUNK_SIZE    = 1000   # characters per chunk
CHUNK_OVERLAP = 200    # overlap between consecutive chunks
EMBEDDING_MODEL = "text-embedding-3-small"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _extract_video_id(url_or_id: str) -> str:
    """
    Accept a full YouTube URL or a bare video ID and return just the ID.

    Supported URL formats:
        https://www.youtube.com/watch?v=fNk_zzaMoSs
        https://youtu.be/fNk_zzaMoSs
        https://www.youtube.com/embed/fNk_zzaMoSs
        fNk_zzaMoSs   ← bare ID, returned as-is
    """
    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",       # ?v=ID
        r"youtu\.be/([A-Za-z0-9_-]{11})",    # youtu.be/ID
        r"embed/([A-Za-z0-9_-]{11})",        # embed/ID
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    # If it's already an 11-char ID
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url_or_id):
        return url_or_id

    raise ValueError(
        f"Could not extract a valid YouTube video ID from: '{url_or_id}'\n"
        "Expected a URL like https://www.youtube.com/watch?v=VIDEO_ID "
        "or a bare 11-character video ID."
    )


def _fetch_transcript(video_id: str) -> str:
    """
    Fetch the transcript for a given video ID and return it as plain text.
    Raises TranscriptsDisabled or NoTranscriptFound if unavailable.
    """
    ytt_api = YouTubeTranscriptApi()
    fetched  = ytt_api.fetch(video_id)
    transcript = " ".join(chunk.text for chunk in fetched)
    return transcript


def _split_transcript(transcript: str) -> list:
    """
    Split raw transcript text into overlapping LangChain Document chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.create_documents([transcript])
    return chunks


def _build_vector_store(chunks: list) -> FAISS:
    """
    Embed chunks with OpenAI and store them in a FAISS index.
    """
    embeddings   = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store


# ── Public API ────────────────────────────────────────────────────────────────

def index_video(url_or_id: str) -> dict:
    
    # extract clean video ID
    video_id = _extract_video_id(url_or_id)
    print(f"[indexing] Video ID  : {video_id}")

    # Step 2 – fetch transcript
    print("[indexing] Fetching transcript …")
    transcript = _fetch_transcript(video_id)
    print(f"[indexing] Transcript: {len(transcript)} characters")

    # Step 3 – chunk
    print("[indexing] Splitting into chunks …")
    chunks = _split_transcript(transcript)
    print(f"[indexing] Chunks    : {len(chunks)}")

    # Step 4 – embed + index
    print("[indexing] Building vector store …")
    vector_store = _build_vector_store(chunks)
    print("[indexing] Done ✓")

    return {
        "video_id"    : video_id,
        "transcript"  : transcript,
        "chunks"      : chunks,
        "vector_store": vector_store,
    }


