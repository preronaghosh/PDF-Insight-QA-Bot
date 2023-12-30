from flask import current_app
from threading import Thread
from queue import Queue
from app.chat.callbacks.stream import StreamingHandler

"""
    StreamableChain can be used as a base chain to build other kinds of streamable chains. 
    Example: ConversationalStreamableChain, etc.
"""
class StreamableChain:
    def stream(self, input):
        queue = Queue()
        handler = StreamingHandler(queue)

        # run the chain in a separate thread
        def run_chain(app_context):
            app_context.push()
            self(input, callbacks=[handler]) 
        
        Thread(target=run_chain, args=[current_app.app_context()]).start()

        # return a generator from new token callback that outputs string values
        while True:
            token = queue.get()
            if token is None:
                break
            yield token