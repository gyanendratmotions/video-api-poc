from fastapi import UploadFile, File
from backend.model.models import IMPROVED_TRANSCRIPT,VIDEO_TRANSCRIPT
from backend.services.services import clone_video_with_transcript,transcript_improvement_logic
from backend.services.vid2vid import generate_video_logic


async def get_transcript(file: UploadFile = File(...),want_cloning: bool = True):
    transcript= await clone_video_with_transcript(file,want_cloning)
    return transcript


async def transcript_improvement(data: IMPROVED_TRANSCRIPT):
    transcript = data.transcript
    feedback = data.feedback
    transformed_transcript = await transcript_improvement_logic(transcript, feedback)
    return {"improved_transcript": transformed_transcript}

async def generate_video(data: VIDEO_TRANSCRIPT):
    generated_video_path = await generate_video_logic(data.transcript, data.cloned_voice_id)
    return {"generated_video_path": generated_video_path}