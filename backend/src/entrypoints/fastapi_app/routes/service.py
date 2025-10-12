from fastapi import APIRouter

from src.domain import SubjectName

router = APIRouter(tags=["Служебные функции ⚙️"])


@router.get(
    "/subjects",
    summary="Получить список доступных предметов",
    responses={200: {"description": "Список названий предметов", "model": list[str]}},
)
def get_available_subjects():
    return [subject for subject in SubjectName]
