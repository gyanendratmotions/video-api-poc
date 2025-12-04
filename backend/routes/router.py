from fastapi import APIRouter,UploadFile, File
from backend.services.services import save_uploaded_file
import os


async def upload_video(file: UploadFile = File(...)):
    saved_path = await save_uploaded_file(file)

    return {
        "status": "success",
        "saved_as": os.path.basename(saved_path),
        "path": saved_path
    }



# @router.get("/{user_id}")
def get_user(user_id: int):
    pass