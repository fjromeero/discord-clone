from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import resend

from app.api.main import api_router
from app.core.config import settings


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

resend.api_key = settings.SMTP_TOKEN

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"Hello": "World"}