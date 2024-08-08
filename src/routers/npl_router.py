
from fastapi import APIRouter

from ..models.prompt import Prompt
from ..services.npl_service import NplService
from ..services.npl_service_openai_impl import NplServiceOpenaiImpl


router = APIRouter()

@router.post("/prompt", tags=["npl"])
async def answer_question(body: Prompt):
    service: NplService = NplServiceOpenaiImpl()
    return service.answer(question=body.prompt)