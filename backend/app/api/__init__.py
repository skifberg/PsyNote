from fastapi import APIRouter
from . import psychometrics, ai_psychology

router = APIRouter()

router.include_router(psychometrics.router)
router.include_router(ai_psychology.router)

__all__ = ["router"]