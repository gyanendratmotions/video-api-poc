from fastapi import APIRouter
from backend.routes.router import upload_video
router = APIRouter()

router.post("/upload-video")(upload_video)