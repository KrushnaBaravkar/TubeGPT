import re
from typing import Union
import os

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv() 



CHUNK_SIZE    = 1000   
CHUNK_OVERLAP = 200    
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def _extract_video_id(url_or_id: str) -> str:

    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",       
        r"youtu\.be/([A-Za-z0-9_-]{11})",    
        r"embed/([A-Za-z0-9_-]{11})",        
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url_or_id):
        return url_or_id

    raise ValueError(
        f"Could not extract a valid YouTube video ID from: '{url_or_id}'\n"
        "Expected a URL like https://www.youtube.com/watch?v=VIDEO_ID "
        "or a bare 11-character video ID."
    )


def _fetch_transcript(video_id: str) -> str:
    ytt_api = YouTubeTranscriptApi()
    fetched  = ytt_api.fetch(video_id)
    transcript = " ".join(chunk.text for chunk in fetched)
    return transcript


def _split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.create_documents([transcript])
    return chunks


def _build_vector_store(chunks: list) -> FAISS:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("check ---------- Embeddings generated ------------")

    vector_store = FAISS.from_documents(chunks, embeddings)

    print("check --------- Vector store created ------------")

    return vector_store


def index_video(url_or_id: str) -> dict:
    
    video_id = _extract_video_id(url_or_id)
    print(f"[indexing] Video ID  : {video_id}")

    print("[indexing] Fetching transcript …")
    transcript = _fetch_transcript(video_id)
    print(f"[indexing] Transcript: {len(transcript)} characters")

    print("[indexing] Splitting into chunks …")
    chunks = _split_transcript(transcript)
    print(f"[indexing] Chunks    : {len(chunks)}")

    print("[indexing] Building vector store …")
    vector_store = _build_vector_store(chunks)
    
    return {
        "video_id"    : video_id,
        "transcript"  : transcript,
        "chunks"      : chunks,
        "vector_store": vector_store,
    }



