class Process(object):
    def __init__(self, listener, processor, executor):
        self._listener = listener
        self._processor = processor
        self._executor = executor

    def run(self):
        for input in self._listener.listen():
            self.execute(self._processor.process, input)

    def process(self, input):
        return self._processor.process(input)

    def execute(self, callable, input):
        return self._executor.execute(callable, input)
