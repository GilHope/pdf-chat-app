class TraceableChain:
    def __call__(self, *args, **kwargs):
        print(kwargs["metadata"])
        return super().__call__(*args, **kwargs)