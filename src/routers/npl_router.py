import logging
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import PlainTextResponse

from .docs.prompt_responses_examples import answer_question_responses
from ..models.prompt import Prompt
from ..services.npl_service import NplService
from ..services.npl_service_openai_impl import NplServiceOpenaiImpl

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/prompt",
             response_class=PlainTextResponse,
             tags=["npl"], 
             summary="NPL Endpoint", 
             description="This endpoint allow the user to talk with data by asking information in natural language.",
             responses=answer_question_responses
             )
async def answer_question(body: Prompt) -> str:
    service: NplService = NplServiceOpenaiImpl()
    try:
        return service.answer(question=body.prompt)
    except HTTPException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
