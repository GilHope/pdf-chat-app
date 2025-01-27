class TraceableChains:
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)