from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from db_api import get_db_message, get_constructor_by_token, create_event
from keyboards import get_service_menu, main_menu, get_category_menu, get_staff_menu
from state import Order


async def cmd_start(message: types.Message, state: FSMContext, **kwargs):
    """"""
    token = Bot.get_current()._token
    text = await get_db_message(text_id='hello', token=token)
    print('kwargs', kwargs, text)
    await message.answer(text, reply_markup=main_menu)


async def contacts(message: types.Message, state: FSMContext):
    """Сообщение на нажатие кнопки Контакты"""
    print('Контакты')
    token = Bot.get_current()._token
    text = await get_db_message(text_id='contacts', token=token)
    await message.answer(text)


async def category(message: types.Message, state: FSMContext):
    """Начало приема заявок (сообщение на нажатие кнопки Добавить заявку) - вопрос: выберите категорию"""
    print('категории')
    await state.reset_data()
    await state.reset_state()
    token = Bot.get_current()._token  # текущий токен
    text = await get_db_message('add_category', token=token)  # запрашиваем сообщение
    constructor = await get_constructor_by_token(token)
    await state.update_data(constructor=constructor)  # сохраняем данные конструктора
    menu = await get_category_menu(constructor)  # генерируем меню
    await message.answer(text, reply_markup=menu)
    await Order.S1.set()


async def service(query: CallbackQuery, state: FSMContext, ):
    await query.answer()
    print(query.data)
    print('услуги')
    await state.update_data(category=query.data)
    token = Bot.get_current()._token
    text = await get_db_message('add_service', token=token)
    data = await state.get_data()
    print(data)
    menu = await get_service_menu(category=query.data, constructor=data['constructor'])
    await query.message.edit_text(text, reply_markup=menu)
    await Order.S2.set()


async def staff(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await state.update_data(service=query.data)
    print('сотрудники')
    token = Bot.get_current()._token
    text = await get_db_message('add_staff', token=token)
    data = await state.get_data()

    menu = await get_staff_menu(category=data['category'], service=query.data, constructor=data['constructor'])
    await query.message.edit_text(text, reply_markup=menu)
    await Order.S3.set()


async def add_date(query: CallbackQuery, state: FSMContext):
    await state.update_data(staff=query.data)
    # await query.answer()
    await query.answer()
    print('дата НА')
    token = Bot.get_current()._token
    text = await get_db_message('add_date', token=token)

    await query.message.answer(text)
    # await Order.S1.set()
    await Order.S4.set()


async def add_name(message: types.Message, state: FSMContext):
    txt = message.text
    await state.update_data(date=txt)
    token = Bot.get_current()._token
    text = await get_db_message('add_name', token=token)

    await message.answer(text)
    await Order.S5.set()


async def add_phone(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    token = Bot.get_current()._token
    text = await get_db_message('add_phone', token=token)
    await message.answer(text)
    await Order.S6.set()


async def result(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    token = Bot.get_current()._token
    event = await create_event(data)
    text = await get_db_message('completed', token=token)
    await message.answer(f'{text}\n{event}')
    await state.finish()


async def cancel(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await state.finish()
    token = Bot.get_current()._token
    text = await get_db_message('cancel', token=token)
    await query.message.answer(text)


async def another_msg(message: types.Message, state: FSMContext):
    await state.reset_data()
    await state.reset_state()
    token = Bot.get_current()._token
    text = await get_db_message('another_msg', token=token)
    await message.answer(text)
