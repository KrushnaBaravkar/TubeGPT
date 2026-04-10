from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

# Local LLM
llm = ChatOllama(
    model="llama3.2",
    temperature=0.2
)

augmentation_prompt = PromptTemplate(
    template="""
You are a context optimizer.

Your job is to extract and refine ONLY the most relevant information
from the given context with respect to the question.

Remove irrelevant parts. Keep it concise and useful.

Context:
{context}

Question:
{question}

Return only the refined context.
""",
    input_variables=["context", "question"]
)

def augment_context(context: str, question: str) -> str:
    """
    Step 2: Augmentation (NEW)
    Refines retrieved context using LLM
    """
    prompt_text = augmentation_prompt.format(
        context=context,
        question=question
    )

    response = llm.invoke(prompt_text)

    return response.content if hasattr(response, "content") else str(response)
