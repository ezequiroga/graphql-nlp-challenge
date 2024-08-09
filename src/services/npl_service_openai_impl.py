
import logging
from fastapi import HTTPException
from openai import OpenAIError

from ..utils.cons import Cons
from .npl_service import NplService
from langchain_experimental.agents import create_csv_agent
from langchain_openai import OpenAI
from ..config.envs import Envs

class NplServiceOpenaiImpl(NplService):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def answer(self, question) -> str:
        self.__sanity_check(question)

        question_wrapper = self.__wrapper_question_promp(question)

        return self.__callOpenAIHelper(question_wrapper)['output']
        
    def __sanity_check(self, question):
        """
        This function should be robust enough to check if the question is valid or not.
        This is a naive implementation and should be improved.
        """

        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        validate_question_promp = self.__wrapper_validate_question_promp(question)

        answer = self.__callOpenAIHelper(validate_question_promp)

        if answer['output'].lower() != "yes":
            raise HTTPException(status_code=400, detail="Invalid question")
    
    def __wrapper_question_promp(self, question):
        return """
        Answer the following question using the data from the CSV file:
        {question}

        You must use the following mapping for the columns. 
        Bear in mind that the structure is 'column_name_in_csv: valid_column_value'.
        You must check column names agains the 'valid_column_value' to answer the question.
        Mapping:
        {mapping}

        Answer the question follwing theses rules:
        - aswer exactly the question,
        - be concise and clear,
        - using the data from the CSV file, 
        - the mapping provided,
        - use only the columns map in the mapping
        - using only the columns that are relevant to the question
        """.format(question=question, mapping=Cons.COLUMN_MAPPING)

    def __wrapper_validate_question_promp(self, question):
        return """
        Is the following question a valid one for consuming data from the CSV file: 
        {question}

        You must use the following mapping for the columns. 
        Bear in mind that the structure is 'column_name_in_csv: valid_column_value'.
        You must check column names agains the 'valid_column_value' to answer the question.
        Mapping:
        {mapping}

        Answer the question follwing theses rules:
        - answering only with 'yes' or 'no', 
        - looking into the data from the CSV file, 
        - the mapping provided,
        - use only the columns map in the mapping
        - using only the columns that are relevant to the question
        """.format(question=question, mapping=Cons.COLUMN_MAPPING)
        
    def __callOpenAIHelper(self, question):
        try:
            agent = create_csv_agent(
                OpenAI(temperature=0), 
                Envs.get_csv_file_path(), 
                verbose=True,
                allow_dangerous_code=True
            )

            return agent.invoke(question)
        except OpenAIError as e:
            self.logger.error(e)
            raise HTTPException(status_code=400, detail=str(e))
