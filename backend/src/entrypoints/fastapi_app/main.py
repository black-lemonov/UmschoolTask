from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

from src.adapters.orm import start_mappers
from src.entrypoints.fastapi_app.routes import student, records, service


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_mappers()
    yield
    clear_mappers()


app = FastAPI(title="Баллы по ЕГЭ 🎓", lifespan=lifespan)

app.include_router(student.router)
app.include_router(records.router)
app.include_router(service.router)
