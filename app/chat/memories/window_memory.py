from langchain.memory import ConversationBufferWindowMemory
from app.chat.memories.histories.sql_history import SqlMessageHistory

def build_window_memory(chat_args):
    return ConversationBufferWindowMemory(
        memory_key="chat_history",
        output_key="answer",
        return_messages=True,
        chat_memory=SqlMessageHistory(
            conversation_id=chat_args.conversation_id
        ),
        k=2
    )