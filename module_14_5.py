from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from pyexpat.errors import messages
from crud_functions import *
import sqlite3

api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage= MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
button3 = KeyboardButton(text="Купить")
button4 = KeyboardButton(text="Регистрация")
kb.add(button)
kb.add(button2)
kb.add(button3)
kb.add(button4)

kb_inline = InlineKeyboardMarkup()
button_inline = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_inline2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

kb_inline.add(button_inline)
kb_inline.add(button_inline2)


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_inline)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

kb_inline2 = InlineKeyboardMarkup()

button_inline3 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button_inline4 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button_inline5 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button_inline6 = InlineKeyboardButton(text='Product4', callback_data='product_buying')

kb_inline2.add(button_inline3)
kb_inline2.add(button_inline4)
kb_inline2.add(button_inline5)
kb_inline2.add(button_inline6)


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    #files = 'files/Askorbin.png', 'files/Calcium.png', 'files/multi.png', 'files/vitaminC.png'
    for index, product in enumerate(get_all_products()):
        await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
        with open(f'{index+1}.png', "rb") as f:
            await message.answer_photo(f)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_inline2)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'Привет, {message.from_user.username}! Я бот помогающий твоему здоровью.', reply_markup=kb)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    result = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] - 161
    await message.answer(f'Расчитанное количество каллорий: {result}')
    await state.finish()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит): ')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer('Введите свой email: ')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
   await state.update_data(email=message.text)
   await message.answer('Введите свой возраст: ')
   await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
   await state.update_data(age=message.text)
   data = await state.get_data()
   add_users(data['username'], data['email'], data['age'])
   await message.answer('Регистрация успешна ')
   await RegistrationState.age.set()
   await state.finish()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')










if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)



