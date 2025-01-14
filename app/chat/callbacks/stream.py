from langchain.callbacks.base import BaseCallbackHandler

class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_chat_model_start(self, serialized, messages, run_id, **kwargs):
        if serialized["kwargs"]["streaming"]:
            print("This is a streaming model! I should lsiten to events with a run_id of ", run_id)

    def on_llm_new_token(self, token, **kwargs):
        self.queue.put(token)

    def on_llm_end(self, response, **kwargs):
        self.queue.put(None)

    def on_llm_error(self, error, **kwargs):
        self.queue.put(None)