
from fastapi import HTTPException
from openai import OpenAIError

from src.utils.cons import Cons
from .npl_service import NplService
from langchain_experimental.agents import create_csv_agent
from langchain_openai import OpenAI
from ..config.envs import Envs

class NplServiceOpenaiImpl(NplService):
    def answer(self, question) -> str:
        self.__sanity_check(question)

        question_wrapper = """
        Answer the following question using the data from the CSV file:
        {question}

        You must use the following mapping for the columns:
        {mapping}

        Answer the question follwing theses rules:
        - in a way that the user can understand, 
        - using the data from the CSV file, 
        - the mapping provided,
        - use only the columns map in the mapping
        - using only the columns that are relevant to the question
        """

        return self.__callOpenAIHelper(question_wrapper.format(
            question=question, 
            mapping=Cons.COLUMN_MAPPING
        ))
        
    def __sanity_check(self, question):
        """
        This function should be robust enough to check if the question is valid or not.
        This is a naive implementation and should be improved.
        """

        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        validate_question_promp = """
        Is the following question a valid one for consuming data from the CSV file: 
        {question}

        You must use the following mapping for the columns:
        {mapping}

        Answer the question follwing theses rules:
        - answering only with 'yes' or 'no', 
        - looking into the data from the CSV file, 
        - the mapping provided,
        - use only the columns map in the mapping
        - using only the columns that are relevant to the question
        """

        answer = self.__callOpenAIHelper(validate_question_promp.format(
            question=question, 
            mapping=Cons.COLUMN_MAPPING
        ))

        if answer.lower() != "yes":
            raise HTTPException(status_code=400, detail="Invalid question")

        
    def __callOpenAIHelper(self, question):
        try:
            agent = create_csv_agent(
                OpenAI(temperature=0), 
                Envs.get_csv_file_path(), 
                verbose=True,
                allow_dangerous_code=True
            )

            return agent.run(question)
        except OpenAIError as e:
            raise HTTPException(status_code=400, detail=str(e))
