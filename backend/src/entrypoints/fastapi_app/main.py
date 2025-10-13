import sys
from contextlib import asynccontextmanager

from loguru import logger
from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

from src.adapters.orm import start_mappers
from src.entrypoints.fastapi_app.routes import student, records, service


logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{level}</green>:<cyan>{function:>15}</cyan> - <level>{message}</level>"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Initializing mappers...")
        start_mappers()
        logger.info("Mappers initialized")
        yield
        clear_mappers()
    except Exception as e:
        logger.error(f"Error during startup {str(e)}")


app = FastAPI(title="Баллы по ЕГЭ 🎓", lifespan=lifespan)

app.include_router(student.router)
app.include_router(records.router)
app.include_router(service.router)
