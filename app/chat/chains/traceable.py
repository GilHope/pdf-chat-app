class TraceableChains:
    def __call__(self, *args, **kwargs):
        print("HI THERE!")
        return super().__call__(*args, **kwargs)