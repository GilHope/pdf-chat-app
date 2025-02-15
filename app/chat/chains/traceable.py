from langfuse.model import CreateTrace
from app.chat.tracing.langfuse import langfuse

class TraceableChain:
    def __call__(self, *args, **kwargs):
        trace = langfuse.trace(
            CreateTrace(
                id=self.metadata["conversation_id"],
                metadata=chat_args.metadata
            )
        )

        callbacks = kwargs.get("callbacks", [])
        callbacks.append(trace.getNewCallback())
        kwargs["callbacks"] = callbacks

        return super().__call__(*args, **kwargs)