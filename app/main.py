from fastapi import FastAPI
from app.routers import chat, generation
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # or specific localhost origin for security later
    allow_credentials=True,
    allow_methods=["*"],         # <-- Allows OPTIONS
    allow_headers=["*"],         # <-- Allows content-type etc.
)


app.include_router(chat.router, prefix="/api")
app.include_router(generation.router, prefix="/api")
