from langchain.chains import ConversationalRetrievalChain
from app.chat.chains.streamable import StreamableChain
from app.chat.chains.traceable import TraceableChain

"""
    Specific class built for ConversationalChains with Streaming capabilities.
    No custom behaviours defined.
"""
class StreamingConversationalRetrievalChain(TraceableChain, StreamableChain, ConversationalRetrievalChain):
    pass