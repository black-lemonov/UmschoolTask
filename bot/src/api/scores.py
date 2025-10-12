import aiohttp

from src import config, exc


async def get_available_subjects() -> list[str]:
    """
    Получить список доступных предметов из API
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{config.get_base_api()}/subjects") as response:
            if response.status == 200:
                data = await response.json()
                return data
            return []
        

async def create_subject_record(subjectname: str, score: int, studentid: int) -> None:
    """
    Отправить запрос на создание записи по предмету
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{config.get_base_api()}/records",
            json={
                "subjectname": subjectname,
                "score": score,
                "studentid": studentid,
            },
        ) as response:
            if response.status == 200:
                return
            elif response.status == 400:
                raise exc.AlreadyExists("Запись по предмету уже существует!")
            elif response.status == 401:
                raise exc.Unauthorized("Ошибка! Вы не зарегистрированы!")
            elif response.status == 422:
                raise exc.WrongArguments("При выборе предмета или вводе баллов была допущена ошибка. Повторите ввод.")


async def get_student_records(studentid: int) -> dict[str, int]:
    """
    Отправить запрос на получение всех записей ученика
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{config.get_base_api()}/scores",
            params={"studentid": studentid},
        ) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 401:
                return await exc.Unauthorized("Вы не зарегистрированы")