from pydantic import BaseModel
from langchain.schema import BaseChatMessageHistory
from app.web.api import (
    get_messages_by_conversation_id,
    add_message_to_conversation
)

""" 
    This custom class will get ChatHistory from SQL database within the backend code 
    Return all existing messages tied to one conversation_id or add a new message to the db 
"""
class SqlMessageHistory(BaseChatMessageHistory, BaseModel):
    conversation_id: str # this is what we see under the history tab of one user using a pdf

    @property
    def messages(self):
        return get_messages_by_conversation_id(self.conversation_id)

    # Adds new message to the SQL database
    def add_message(self, message):
        return add_message_to_conversation(
            conversation_id=self.conversation_id,
            role=message.type,
            content=message.content
        )

    def clear(self):
        pass