import abc


class QueryService(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'get_all') and callable(subclass.get_all)

    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError
