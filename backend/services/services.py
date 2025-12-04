from backend.constants.constant import UPLOAD_DIR
from fastapi import UploadFile
import os

async def save_uploaded_file(file: UploadFile) -> str:
    """
    Saves an uploaded file into the UPLOAD_DIR and returns the saved path.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return file_path