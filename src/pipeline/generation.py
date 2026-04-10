from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

llm = ChatOllama(
    model="llama3.2",
    temperature=0.2
)

prompt = PromptTemplate(
    template = """
Answer the question using only the provided context.
Stay faithful to the context and avoid adding unsupported details.

Guidelines:
1. If the context directly answers the question, give a direct and well-structured answer.
2. If the context is partially relevant, use only the relevant parts.
3. If the context does not contain enough information, say:
   "Query is not matching the context metched."
4. After that, you may add a brief general response only if it does not conflict with the context.
5. Keep the answer concise, clear, and fact-based.

query:
{query}
context: 
{context}
""",
    input_variables=["query", "context"] 
)

def _generation(query:str, context:str)->str :
    input_prompt = prompt.format(
        query = query,
        context = context
    )

    output = llm.invoke(input_prompt)

    return output.content