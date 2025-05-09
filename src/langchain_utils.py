from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.chroma_utils import vectorstore
# from src.prompt import contextualize_q_system_prompt
## setup cache system
from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
set_llm_cache(SQLiteCache(database_path=".langchain_cache.db"))
##Setting up retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

##Output Parser
output_parser = StrOutputParser()

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)
## Setting Up Prompts
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# qa_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful medical assistant helping users find the right doctor. Use the following context to answer the user's question. if you don't have any answer please truthfully say i don't have the information. Answer should be short and precise, don't need to elaborate any answer."),
#     ("system", "Context: {context}"),
#     MessagesPlaceholder(variable_name="chat_history"),
#     ("human", "{input}")
# ])
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are Genie, a helpful medical assistant that helps users find suitable doctors.\n"
     "You are expected to handle the conversation end-to-end.\n\n"
     "Your goals:\n"
     "1. Understand the user's medical issue (symptom)\n"
     "2. Get their location\n"
     "3. Infer or ask for the type of specialist if needed\n"
     "4. Ask follow-up questions until you have all 3\n"
     "5. Once ready, use the context below to recommend up to 3 matching doctors.\n\n"
     "Instructions:\n"
     "- Always respond conversationally\n"
     "- Be polite and concise\n"
     "- Once you have all the information, return a list of doctors with: Name, Specialization, Hospital, Location, Availability\n"
     "- If no doctor fits, say so.\n"
     "- Do not hallucinate. Use only the provided context.\n"
     "- If unsure, ask the user politely."),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])


def get_rag_chain(model_name:str="gemini-2.0-flash",model_provider:str="google_genai"):
    llm = init_chat_model(model=model_name,model_provider=model_provider)
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)    
    return rag_chain
