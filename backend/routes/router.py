from fastapi import APIRouter,UploadFile, File
from backend.services.services import clone_video_with_transcript,transcript_improvement_logic
from backend.services.vid2vid import generate_video_logic
import os


async def get_transcript(file: UploadFile = File(...),want_cloning: bool = True):
    transcript,cloned_voice_id = await clone_video_with_transcript(file,want_cloning)
    return {"transcript": transcript, "cloned_voice_id": cloned_voice_id ,"original_filename": "jbdcabchahcbh"}


async def transcript_improvement(transcript: str,feedback: str):
    transformed_transcript = await transcript_improvement_logic(transcript, feedback)
    return {"improved_transcript": transformed_transcript}


async def generate_video(transcript: str,cloned_voice_id: str | None=None):
    generated_video_path = await generate_video_logic(transcript, cloned_voice_id)
    return {"generated_video_path": generated_video_path}