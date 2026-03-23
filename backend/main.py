from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.query import router as query_router

app = FastAPI()

app.include_router(query_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"status": "ok"}