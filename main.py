from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.ai_response_routes import router as ai_response_router
from routes.email_routes import router as email_router
from routes.conversation_routes import router as conversation_router
from db import engine
import os
from models import Base
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

#cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://lunexbot.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(ai_response_router)
app.include_router(email_router)
app.include_router(conversation_router)
# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)