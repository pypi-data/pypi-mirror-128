import abc
from typing import Any


class RequestArgumentsAdapter(object):

    @abc.abstractmethod
    def adapt(self, *args, **kwargs) -> Any:
        pass


class NoopRequestArgumentsAdapter(RequestArgumentsAdapter):

    def adapt(self, *args, **kwargs) -> Any:
        return args, kwargs
