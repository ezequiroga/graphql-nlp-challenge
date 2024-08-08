
from fastapi import APIRouter, HTTPException

from ..models.prompt import Prompt
from ..services.npl_service import NplService
from ..services.npl_service_openai_impl import NplServiceOpenaiImpl


router = APIRouter()

@router.post("/prompt", tags=["npl"])
async def answer_question(body: Prompt):
    service: NplService = NplServiceOpenaiImpl()
    try:
        return service.answer(question=body.prompt)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
