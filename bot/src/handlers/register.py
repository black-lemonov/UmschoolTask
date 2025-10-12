from aiogram import Router, filters, types
from aiogram.fsm import state, context

from src import exc
from src.api import register as api

router = Router()


class RegisterState(state.StatesGroup):
    entering_firstname = state.State()
    entering_lastname = state.State()


@router.message(filters.StateFilter(None), filters.Command("register"))
async def register(message: types.Message, state: context.FSMContext):
    try:
        await api.try_to_signin(message.from_user.id)
        await message.answer("Вы уже зарегистрированы")
    except exc.Unauthorized:
        await message.answer("Введите имя:")
        await state.set_state(RegisterState.entering_firstname)
    except exc.APIError as e:
        await message.answer(str(e))


@router.message(RegisterState.entering_firstname)
async def firstname_entered(message: types.Message, state: context.FSMContext):
    await state.update_data(firstname=message.text)
    await message.answer("Введите фамилию:")
    await state.set_state(RegisterState.entering_lastname)


@router.message(RegisterState.entering_lastname)
async def lastname_entered(message: types.Message, state: context.FSMContext):
    try:
        user_data = await state.get_data()
        firstname = user_data["firstname"]
        lastname = message.text
        await api.try_to_signup(firstname, lastname, message.from_user.id)
        await message.answer("Вы зарегистрированы!")
        await state.clear()
    except exc.AlreadyExists as e:
        await message.answer(str(e))
        await state.clear()
    except exc.WrongArguments as e:
        await message.answer(str(e))
        await message.answer("Введите имя:")
        await state.set_state(RegisterState.entering_firstname)
    except exc.APIError as e:
        await message.answer(str(e))
        await state.clear()
