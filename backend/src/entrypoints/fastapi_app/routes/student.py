from fastapi import APIRouter, Response, status
from loguru import logger

from src import services
from src.adapters import repository
from src.entrypoints.fastapi_app import deps
from src.entrypoints.fastapi_app.schemas import student as schemas


router = APIRouter(tags=["Профиль 👤"])


@router.post(
    "/signup",
    summary="Создать запись ученика",
    responses={
        200: {
            "description": "Успешное создание записи",
            "model": schemas.StudentSignedUp,
        },
        400: {
            "description": "Ученик уже существует",
            "model": schemas.StudentAlreadySignedUp,
        },
    },
)
async def signup(
    student: schemas.SignUpStudent, session: deps.SessionDep, response: Response
):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    try:
        logger.info(f"Signing up student {student.studentid} ...")
        await services.signup(
            student.firstname,
            student.lastname,
            student.studentid,
            student_repo,
            session,
        )
    except services.StudentAlreadyExists as e:
        logger.error(f"Sign up error: {str(e)}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return schemas.StudentAlreadySignedUp()

    return schemas.StudentSignedUp()


@router.post(
    "/signin",
    summary="Войти по id",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Успешный вход", "model": schemas.StudentSignedIn},
        401: {"description": "Вход не выполнен", "model": schemas.StudentDoesNotExist},
    },
)
async def signin(
    student: schemas.SignInStudent, session: deps.SessionDep, response: Response
):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    try:
        logger.info(f"Signing in student {student.studentid} ...")
        await services.signin(student.studentid, student_repo)
    except services.StudentDoesNotExist as e:
        logger.error(f"Sign in error: {str(e)}")
        response.status_code = status.HTTP_404_NOT_FOUND
        return schemas.StudentDoesNotExist()

    return schemas.StudentSignedIn()


@router.put(
    "/student",
    summary="Изменить личные данные пользователя",
    responses={
        200: {
            "description": "Данные успешно обновлены",
            "model": schemas.StudentUpdated,
        },
        401: {"description": "Ученик не найден", "model": schemas.StudentDoesNotExist},
    },
)
async def update_student(
    student: schemas.UpdateStudent, session: deps.SessionDep, response: Response
):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    try:
        logger.info(f"Trying to update student {student.studentid} ...")
        await services.update_student(
            student.firstname,
            student.lastname,
            student.studentid,
            student_repo,
            session,
        )
    except services.StudentDoesNotExist as e:
        logger.error(f"Update student error: {str(e)}")
        response.status_code = status.HTTP_404_NOT_FOUND
        return schemas.StudentDoesNotExist()

    return schemas.StudentUpdated()
