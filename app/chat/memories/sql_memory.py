from langchain.memory import ConversationBufferMemory
from .histories.sql_history import SqlMessageHistory


def build_memory(chat_args):
    return ConversationBufferMemory(
        chat_memory=SqlMessageHistory(conversation_id=chat_args.conversation_id),
        output_key="answer",
        memory_key="chat_history",
        return_messages=True,
    )
