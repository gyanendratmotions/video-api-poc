from pydantic import BaseModel

class IMPROVED_TRANSCRIPT(BaseModel):
    transcript: str
    feedback: str

class VIDEO_TRANSCRIPT(BaseModel):
    transcript: str
    cloned_voice_id: str | None = None