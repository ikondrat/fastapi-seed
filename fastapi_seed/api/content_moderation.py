from typing import Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..services.content_moderation import ContentModerationService

router = APIRouter(prefix="/content-moderation", tags=["content-moderation"])

# Dependency to get the service instance
def get_moderation_service():
    return ContentModerationService()

class ModerationRequest(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    scores: Dict[str, float]
    request_rate: float

@router.post("/moderate", response_model=ModerationResponse)
async def moderate_content(
    request: ModerationRequest,
    service: ContentModerationService = Depends(get_moderation_service)
):
    """Moderate the provided text content and return category scores.
    """
    scores = service.moderate_text(request.text)
    request_rate = service.get_request_rate()

    return ModerationResponse(
        scores=scores,
        request_rate=request_rate
    )
