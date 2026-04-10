import streamlit as st
from indexing import index_video
from retrieval import get_context_from_vector_store
from augmentation import augment_context
from generation import _generation

st.set_page_config(page_title="YouTube RAG QA", layout="wide")

st.title("🎥 YouTube Video Q&A (RAG Pipeline)")
st.write("Ask questions from any YouTube video using your custom pipeline.")

video_url = st.text_input("Enter YouTube Video URL:")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if st.button("Verify video Link"):
    if not video_url:
        st.warning("Please enter a valid YouTube URL")
    else:
        with st.spinner("Validating link... ⏳"):
            result = index_video(video_url)
            st.session_state.vector_store = result["vector_store"]

        st.success("✅ Video link validated successfully!")


query = st.text_input("Ask a question about the video:")

if st.button("Get Answer"):
    if st.session_state.vector_store is None:
        st.error("⚠️ Please index a video first.")
    elif not query:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Processing... 🤖"):
            # Retrieval
            retrieved_context = get_context_from_vector_store(
                st.session_state.vector_store, query
            )

            # Augmentation
            final_context = augment_context(retrieved_context, query)

            # Generation
            answer = _generation(query, final_context)

        st.subheader("📌 Answer:")
        st.write(answer)

        # with st.expander("🔍 Debug Info"):
        #     st.write("### Retrieved Context")
        #     st.write(retrieved_context)

        #     st.write("### Final Augmented Context")
        #     st.write(final_context)