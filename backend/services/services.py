from backend.constants.constant import UPLOAD_DIR,LLAMA_VERSATILE_MODEL
from backend.constants.environ import ASSEMBLY_API_KEY,GROQ_API_KEY
import shutil
import assemblyai as aai
from fastapi import UploadFile
from groq import Groq
import os

aai.settings.api_key = ASSEMBLY_API_KEY

client = Groq(api_key=GROQ_API_KEY)

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


async def transcript_improvement_logic(transcript, feedback) -> str:
    """
    Improves a transcript based on provided feedback using a Groq LLM.
    """

    system_prompt = (
        "You are a professional transcript editor.\n"
        "Your task is to revise a video transcript strictly according to user feedback.\n"
        "Preserve the original meaning, intent, and factual content.\n"
        "Do not add new information or remove important details unless explicitly requested.\n"
        "Maintain a natural, spoken-language flow.\n"
        "Apply only the changes requested in the feedback.\n\n"
        "Return ONLY the revised transcript.\n"
        "Do NOT include explanations, markdown, or commentary."
    )

    user_prompt = (
        f"Original Transcript:\n"
        f"\"\"\"\n{transcript}\n\"\"\"\n\n"
        f"User Feedback:\n"
        f"\"\"\"\n{feedback}\n\"\"\"\n\n"
        f"Revise the transcript according to the feedback."
    )

    chat_completion = client.chat.completions.create(
        model=LLAMA_VERSATILE_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    return chat_completion.choices[0].message.content.strip()

