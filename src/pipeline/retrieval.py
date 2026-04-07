from typing import List
from langchain_core.documents import Document

def get_context_from_vector_store(vector_store, query: str, k: int = 4) -> str:
    """
    Take a query, retrieve the most relevant chunks from the vector store,
    and return them as one combined context string.
    """
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )

    docs: List[Document] = retriever.invoke(query)

    context = "\n\n".join(doc.page_content for doc in docs)
    return context