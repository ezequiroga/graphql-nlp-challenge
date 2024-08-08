
from .npl_service import NplService


class NplServiceOpenaiImpl(NplService):
    def answer(self, question) -> str:
        return "Use OpenAI to answer questions"