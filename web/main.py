from fastapi import FastAPI
from pydantic import BaseModel
from parser.answer_module import SkyAnswers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Определение модели запроса
class RoomRequest(BaseModel):
    roomName: str

@app.post("/get_answers/")
async def get_answers(request: RoomRequest):
    answers_module = SkyAnswers(request.roomName)
    answers = await answers_module.get_answers()
    more_info = await answers_module.get_room_info()
    return answers, more_info
