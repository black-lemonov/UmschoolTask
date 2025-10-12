from aiogram import Router, filters, types
from aiogram.fsm import state, context

from src import exc
from src.api import scores as api
from src.keyboards import scores as keyboards

router = Router()


class EnterScoresState(state.StatesGroup):
    choosing_subject = state.State()
    entering_score = state.State()


@router.message(filters.StateFilter(None), filters.Command("enter_scores"))
async def enter_scores(message: types.Message, state: context.FSMContext):
    subjects = await api.get_available_subjects()
    await message.answer(
        "Выбери предмет:", reply_markup=keyboards.get_subjects_keyboard(subjects)
    )
    await state.set_state(EnterScoresState.choosing_subject)


@router.callback_query(EnterScoresState.choosing_subject)
async def subject_chosen(callback: types.CallbackQuery, state: context.FSMContext):
    await state.update_data(subjectname=callback.data)
    await callback.message.answer("Введи баллы:")
    await callback.answer()
    await state.set_state(EnterScoresState.entering_score)


@router.message(EnterScoresState.entering_score)
async def score_entered(message: types.Message, state: context.FSMContext):
    try:
        score = int(message.text)
    except ValueError:
        await message.answer("Баллы должны быть числом! Повторите ввод.")
        return
    user_data = await state.get_data()
    subjectname = user_data["subjectname"]

    try:
        await api.create_subject_record(subjectname, score, message.from_user.id)
    except (exc.Unauthorized, exc.AlreadyExists) as e:
        await message.answer(str(e))
        await state.clear()
    except exc.WrongArguments as e:
        await message.answer(str(e))
        await message.answer("Предмет:", reply_markup=keyboards.get_subjects_keyboard())
        await state.set_state(EnterScoresState.choosing_subject)

    await message.answer("Запись добавлена")
    await state.clear()


@router.message(filters.Command("view_scores"))
async def view_scores(message: types.Message):
    records = await api.get_student_records(message.from_user.id)
    await message.answer(**keyboards.get_records_list(records).as_kwargs())
