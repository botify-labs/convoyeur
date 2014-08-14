import abc


class AbstractExecutor(object):
    __meta__ = abc.ABCMeta

    @abc.abstractmethod
    def execute(self, callable, *args, **kwargs):
        raise NotImplementedError


class MultiprocessingExecutor(object):
    def __init__(self, nb_processes=None):
        import multiprocessing

        self._pool = multiprocessing.Pool(processes=nb_processes)

    def execute(self, callable, *args, **kwargs):
        self._pool.apply_async(callable, *args, **kwargs)


class ThreadPoolExecutor(object):
    def __init__(self, nb_workers=1):
        from concurrent.futures import ThreadPoolExecutor

        self._executor = ThreadPoolExecutor(max_workers=nb_workers)

    def execute(self, callable, *args, **kwargs):
        return self._executor.submit(callable, *args, **kwargs).result()
