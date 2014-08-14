import abc


class Decorator(object):
    def __init__(self):
        self._inner_processor = None

    def decorate(self, processor):
        self._inner_processor = processor

    def __call__(self, processor):
        self.decorate(processor)
        return self

    def process(self, input):
        if self._inner_processor is not None:
            input = self._inner_processor.process(input)

        return input


class AbstractProcessor(Decorator):
    __meta__ = abc.ABCMeta

    @abc.abstractmethod
    def process(self, input):
        return super(AbstractProcessor, self).process(input)


class DummyProcessor(AbstractProcessor):
    def process(self, task):
        print('{}({})'.format(task.func, task.input))


class EventProcessor(AbstractProcessor):
    def __init__(self, func):
        super(EventProcessor, self).__init__()

        self._func = func

    def process(self, event):
        event = super(EventProcessor, self).process(event)
        return self._func(event)
