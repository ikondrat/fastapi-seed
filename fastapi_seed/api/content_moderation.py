from typing import Dict

from fastapi import APIRouter, Depends, Request
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
    request: Request,
    moderation_request: ModerationRequest,
    service: ContentModerationService = Depends(get_moderation_service)
):
    """Moderate the provided text content and return category scores.
    """
    scores = service.moderate_text(moderation_request.text)

    # Get RPS from middleware
    request_rate = getattr(request.state, "rps", 0.0)

    return ModerationResponse(
        scores=scores,
        request_rate=request_rate
    )
