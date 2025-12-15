from fastapi import APIRouter
from backend.routes.router import get_transcript,transcript_improvement,generate_video
router = APIRouter()

router.post("/get_transcript")(get_transcript)
router.post("/transcript_improvement")(transcript_improvement)

router.post("/generate_video")(generate_video)