from fastapi import APIRouter, Response, status

from src import services
from src.adapters import repository
from src.entrypoints.fastapi_app import deps, schemas


router = APIRouter(tags=["Профиль 👤"])


@router.post(
    "/signup",
    summary="Создать запись ученика",
    responses={
        200: {
            "description": "Успешное создание записи",
            "model": schemas.SuccessMessageResponse,
        },
        400: {
            "description": "Ученик уже существует",
            "model": schemas.ErrorMessageResponse,
        },
    },
)
async def signup(
    student: schemas.SignUpStudent, session: deps.SessionDep, response: Response
):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    try:
        await services.signup(
            student.firstname,
            student.lastname,
            student.studentid,
            student_repo,
            session,
        )
    except services.StudentAlreadyExists as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"msg": str(e)}
    return {"msg": "Запись ученика создана"}


@router.post(
    "/signin",
    summary="Войти по id",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Успешный вход", "model": schemas.SuccessMessageResponse},
        404: {"description": "Ученик не найден", "model": schemas.ErrorMessageResponse},
    },
)
async def signin(
    student: schemas.SignInStudent, session: deps.SessionDep, response: Response
):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    try:
        await services.signin(student.studentid, student_repo)
    except services.StudentDoesNotExist as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": str(e)}
    return {"msg": "Вход выполнен"}


@router.put(
    "/student",
    summary="Изменить личные данные пользователя",
    responses={
        200: {
            "description": "Данные успешно обновлены",
            "model": schemas.SuccessMessageResponse,
        },
        404: {"description": "Ученик не найден", "model": schemas.ErrorMessageResponse},
    },
)
async def update_student(
    student: schemas.UpdateStudent, session: deps.SessionDep, response: Response
):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    try:
        await services.update_student(
            student.firstname,
            student.lastname,
            student.studentid,
            student_repo,
            session,
        )
    except services.StudentDoesNotExist as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": str(e)}
    return {"msg": "Информация обновлена"}
