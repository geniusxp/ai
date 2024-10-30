from datetime import datetime

from sentiment_prediction import predict_message
from project_recommendation import recommend_projects

import oracledb

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from pydantic import BaseModel

connection = oracledb.connect(
    user="rm99565",
    password="140805",
    dsn="oracle.fiap.com.br/orcl")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
async def app_status():
    return 'ok'

@app.post("/event/{event_id}/send-message")
async def send_message(message: str, event_id: int):
    emotion = predict_message(message)

    cursor = connection.cursor()
    cursor.callproc("INCREASE_EVENT_EMOTION", [event_id, emotion])
    connection.commit()
    return emotion

class EventDay(BaseModel):
    date: datetime
    empty: int
    sadness: int
    enthusiasm: int
    neutral: int
    worry: int
    surprise: int
    love: int
    fun: int
    hate: int
    happiness: int
    boredom: int
    relief: int
    anger: int

@app.get("/event/{event_id}")
async def get_event(event_id: int):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM TBL_EVENT_EMOTIONS WHERE EVENT_ID = :id", id=event_id)
    event_days = cursor.fetchall()

    event_day_list = [EventDay(
        date=row[2],
        empty=row[3],
        sadness=row[4],
        enthusiasm=row[5],
        neutral=row[6],
        worry=row[7],
        surprise=row[8],
        love=row[9],
        fun=row[10],
        hate=row[11],
        happiness=row[12],
        boredom=row[13],
        relief=row[14],
        anger=row[15]
    ) for row in event_days]

    return event_day_list

class Project(BaseModel):
    nome: str
    descricao: str
    curso: str
    tipo: str
    segmentos: str
    local: int | str
    horario: str

@app.get("/projects-recommendation")
async def get_recommendation(interests: str):
    projects = recommend_projects(interests).head(5)

    project_list = [Project(
        nome=row["nome"],
        descricao=row["descricao"],
        curso=row["curso"],
        tipo=row["tipo"],
        segmentos=row["segmentos"],
        local=row["local"],
        horario=row["horario"]
    ) for idx, row in projects.iterrows()]

    return project_list
