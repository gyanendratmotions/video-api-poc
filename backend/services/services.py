from backend.constants.constant import UPLOAD_DIR
from backend.constants.environ import ASSEMBLY_API_KEY
import shutil
import assemblyai as aai
from fastapi import UploadFile
import os

print("bchhcd",ASSEMBLY_API_KEY)
aai.settings.api_key = ASSEMBLY_API_KEY

os.makedirs(UPLOAD_DIR, exist_ok=True)

def video_to_transcript(video_path: str) -> str:
    """
    Converts a video file into a transcript using AssemblyAI.
    """

    config = aai.TranscriptionConfig(
        speech_models=["universal"]
    )

    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(video_path)

    if transcript.status == "error":
        raise RuntimeError(transcript.error)

    return transcript.text


async def clone_video_with_transcript(file,want_cloning) -> str:
    """
    Saves an uploaded file into the UPLOAD_DIR and returns the saved path.
    """
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Only video files are allowed")

    video_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # Save uploaded video
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Transcribe video
        transcript_text = video_to_transcript(video_path)

        return {
            "filename": file.filename,
            "transcript": transcript_text
        }

    except Exception as e:
        print(e)

    finally:
        # Optional: cleanup uploaded file
        if os.path.exists(video_path):
            os.remove(video_path)


async def transcript_improvement_logic(transcript,feedback) -> str:
    """
    Placeholder function for transcript improvement logic.
    """
    return None

