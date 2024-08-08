import abc


class NplService(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, '') and callable(subclass.answer)

    @abc.abstractmethod
    def answer(self, question):
        raise NotImplementedError
