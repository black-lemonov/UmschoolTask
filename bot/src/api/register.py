import aiohttp

from src import config, exc


async def try_to_signin(studentid: int) -> None:
    """
    Отправляет запрос на авторизацию,
    если пользователь не существует или клиент не доступен, вызывает исключение
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{config.get_base_api()}/signin",
                json={
                    "studentid": studentid,
                },
            ) as response:
                if response.status == 404:
                    raise exc.Unauthorized("Пользователь не найден")
    except aiohttp.ClientConnectionError:
        raise exc.APIError("Клиент временно недоступен")


async def try_to_signup(firstname: str, lastname: str, studentid: int) -> None:
    """
    Отправляет запрос на регистрацию,
    если пользователь не существует, введены некорректные данные или клиент недоступен, вызывает исключение
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{config.get_base_api()}/signup",
                json={
                    "studentid": studentid,
                    "firstname": firstname,
                    "lastname": lastname,
                },
            ) as response:
                if response.status == 400:
                    raise exc.AlreadyExists("Вы уже зарегистрированы")
                elif response.status == 422:
                    raise exc.WrongArguments("Ошибка при вводе данных. Повторите ввод.")
    except aiohttp.ClientConnectionError:
        raise exc.APIError("Клиент временно недоступен")
