from fastapi import FastAPI
from backend.utils.setup_cors import enable_cors
from backend.routes.api import router

app = FastAPI()

enable_cors(app)

app.include_router(router)