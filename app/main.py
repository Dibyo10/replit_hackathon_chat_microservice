from fastapi import FastAPI
from app.routers import chat, generation

app = FastAPI()

app.include_router(chat.router, prefix="/api")
app.include_router(generation.router, prefix="/api")
