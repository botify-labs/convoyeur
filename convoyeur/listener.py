import abc
import logging


logger = logging.getLogger(__name__)


class AbstractListener(object):
    __meta__ = abc.ABCMeta

    @abc.abstractmethod
    def listen(self):
        pass


class NamedPipeListener(object):
    def __init__(self, path):
        self._path = path
        self._alive = True

    def read(self, pipe):
            return pipe.read().strip()

    def listen(self):
        while self._alive:
            with open(self._path, 'rb') as pipe:
                input = self.read(pipe)

            yield input
