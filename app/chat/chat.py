from langchain.chat_models import ChatOpenAI

from app.chat.models import ChatArgs
from app.chat.vector_stores.pinecone import build_retriever
from app.chat.llms.chatopenai import build_llm
from app.chat.memories.sql_memory import build_memory
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain

"""
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
"""
def build_chat(chat_args: ChatArgs):
    retriever = build_retriever(chat_args) 
    memory = build_memory(chat_args)
    llm = build_llm(chat_args)
    condense_question_llm = ChatOpenAI(streaming=False)

    return StreamingConversationalRetrievalChain.from_llm(
        memory=memory,
        llm=llm,
        retriever=retriever,
        condense_question_llm=condense_question_llm
    )
