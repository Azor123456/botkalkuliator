from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from googletrans import Translator
import asyncio
bot = Bot("7168174207:AAF1MwvTM2BLu0aNQ4itUlhuYYSILKXnpFQ")
dp = Dispatcher(bot,storage=MemoryStorage())
markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.add("как дела?")
markup.add("как тебя зовут?")
markup.add("в каком ты городе?")
markup.add("какой предмет в школе тебе нравится?")
markup.add("что тебе нравится из еды?")
markup.add("твой любимый жанр музыки?")


markup_trans_from = InlineKeyboardMarkup(resize_keyboard=True)
en_button = InlineKeyboardButton("английский", callback_data="from_en")
ispan_button = InlineKeyboardButton("испанский", callback_data="from_spain")
franc_button = InlineKeyboardButton("французский", callback_data="from_franc")
russ_button = InlineKeyboardButton("русский", callback_data="from_ru")
markup_trans_from.add(en_button,ispan_button,franc_button,russ_button)

markup_trans_to = InlineKeyboardMarkup(resize_keyboard=True)
en_button = InlineKeyboardButton("английский", callback_data="to_en")
ispan_button = InlineKeyboardButton("испанский", callback_data="to_spain")
franc_button = InlineKeyboardButton("французский", callback_data="to_franc")
russ_button = InlineKeyboardButton("русский", callback_data="to_ru")
markup_trans_to.add(en_button,ispan_button,franc_button,russ_button)

class CalculatorBotStates(StatesGroup):
    wait_primer = State()
    communication = State()
    wait_dela = State()
    wait_text = State()

@dp.message_handler(commands="calculate")
async def calculate(message: types.Message, state: FSMContext):
    await message.answer("введите пример", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(CalculatorBotStates.wait_primer.state)

@dp.message_handler(commands="translate")
async def translate(message: types.Message, state: FSMContext):
    await message.answer("выберите язык", reply_markup=markup_trans_from)

@dp.message_handler(state=CalculatorBotStates.wait_primer)
async def calculate_primer(message: types.Message, state: FSMContext):
    await message.answer(eval(message.text), reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("привет у меня есть команды /calculate,/help,/communication", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands="communication")
async def communication(message: types.Message, state: FSMContext):
    await message.answer("введи свой вопрос", reply_markup=markup)
    await state.set_state(CalculatorBotStates.communication.state)

@dp.message_handler(state=CalculatorBotStates.communication)
async def calculate_primer(message: types.Message, state: FSMContext):
    if message.text == "как дела?":
        await message.answer('хорошо а у тебя?')
        await state.set_state(CalculatorBotStates.wait_dela.state)
    if message.text == "как тебя зовут?":
        await message.answer("Олег")
    if message.text == "в каком ты городе?":
        await message.answer("я в Красноярске")
    if message.text == "какой предмет в школе тебе нравится?":
        await message.answer("физра,окружающий ииииииииииииииииии русский")
    if message.text == "что тебе нравится из еды?":
        await message.answer ("пастаааа мама мияяяяяя")
    if message.text == "твой любимый жанр музыки?":
        await message.answer ("рок")

@dp.message_handler(commands="help")
async def help(message: types.Message):
    await message.answer("я умею:\n решать примеры и общатся",  reply_markup=types.ReplyKeyboardRemove())

@dp.callback_query_handler(text = "from_en")
async def from_en(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(from_language = "en")
    await bot.send_message(callback.message.chat.id,"выберите язык", reply_markup=markup_trans_to )
    await callback.message.delete()

@dp.callback_query_handler(text = "from_spain")
async def from_spain(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(from_language = "es")
    await bot.send_message(callback.message.chat.id,"выберите язык", reply_markup=markup_trans_to )
    await callback.message.delete()

@dp.callback_query_handler(text="from_franc")
async def from_franc(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(from_language="fr")
    await bot.send_message(callback.message.chat.id, "выберите язык", reply_markup=markup_trans_to)
    await callback.message.delete()

@dp.callback_query_handler(text="from_ru")
async def from_ru(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(from_language="ru")
    await bot.send_message(callback.message.chat.id, "выберите язык", reply_markup=markup_trans_to)
    await callback.message.delete()

@dp.callback_query_handler(text="to_en")
async def to_en(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(to_language = "en")
    await bot.send_message(callback.message.chat.id,"введите сообщение для перевода", reply_markup=types.ReplyKeyboardRemove())
    await callback.message.delete()
    await state.set_state(CalculatorBotStates.wait_text.state)


@dp.callback_query_handler(text="to_spain")
async def to_spain(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(to_language="es")
    await bot.send_message(callback.message.chat.id, "введите сообщение для перевода",
                           reply_markup=types.ReplyKeyboardRemove())
    await callback.message.delete()
    await state.set_state(CalculatorBotStates.wait_text.state)

@dp.callback_query_handler(text="to_franc")
async def to_franc(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(to_language = "fr")
    await bot.send_message(callback.message.chat.id,"введите сообщение для перевода", reply_markup=types.ReplyKeyboardRemove())
    await callback.message.delete()
    await state.set_state(CalculatorBotStates.wait_text.state)

@dp.callback_query_handler(text="to_ru")
async def to_ru(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(to_language = "ru")
    await bot.send_message(callback.message.chat.id,"введите сообщение для перевода", reply_markup=types.ReplyKeyboardRemove())
    await callback.message.delete()
    await state.set_state(CalculatorBotStates.wait_text.state)
@dp.message_handler(state= CalculatorBotStates.wait_text)
async def translate(message: types.Message, state: FSMContext):
    translator = Translator()
    data = await state.get_data()
    text = translator.translate(message.text, src= data["from_language"], dest= data["to_language"])
    await message.answer(text.text)
    await state.finish()



if __name__ == "__main__":
    executor.start_polling(dp)