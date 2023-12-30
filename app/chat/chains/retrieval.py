from langchain.chains import ConversationalRetrievalChain
from app.chat.chains.streamable import StreamableChain

"""
    Specific class built for ConversationalChains with Streaming capabilities.
    No custom behaviours defined.
"""
class StreamingConversationalRetrievalChain(StreamableChain, ConversationalRetrievalChain):
    pass