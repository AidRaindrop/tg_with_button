import logging

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import TOKEN
from utils import TestStates
from messages import MESSAGES

import help_mes as hm
import keyboard as kb
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!", reply_markup=kb.greet_kb2)



@dp.message_handler(commands=['hi3'])
async def process_hi3_command(message: types.Message):
    await message.reply("Третье - добавляем больше кнопок", reply_markup=kb.markup3)

@dp.message_handler(commands=['hi4'])
async def process_hi4_command(message: types.Message):
    await message.reply("Четвертое - расставляем кнопки в ряд", reply_markup=kb.markup4)

@dp.message_handler(commands=['hi5'])
async def process_hi5_command(message: types.Message):
    await message.reply("Пятое - добавляем ряды кнопок", reply_markup=kb.markup5)

@dp.message_handler(commands=['hi6'])
async def process_hi6_command(message: types.Message):
    await message.reply("Шестое - запрашиваем контакт и геолокацию\nЭти две кнопки не зависят друг от друга", reply_markup=kb.markup_request)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(hm.help_message)

@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    await message.reply("Первая инлайн кнопка", reply_markup=kb.inline_kb1)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 2:
        await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
    elif code == 5:
        await bot.answer_callback_query(
            callback_query.id,
            text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉', show_alert=True)
    else:
        await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')

@dp.message_handler(commands=['2'])
async def process_command_2(message: types.Message):
    await message.reply("Отправляю все возможные кнопки", reply_markup=kb.inline_kb_full)

@dp.message_handler(state='*', commands=['setstate'])
async def process_setstate_command(message: types.Message):
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply(MESSAGES['state_reset'])

    if (not argument.isdigit()) or (not int(argument) < len(TestStates.all())):
        return await message.reply(MESSAGES['invalid_key'].format(key=argument))

    await state.set_state(TestStates.all()[int(argument)])
    await message.reply(MESSAGES['state_change'], reply=False)

@dp.message_handler(state=TestStates.TEST_STATE_1)
async def first_test_state_case_met(message: types.Message):
    await message.reply('Первый!', reply=False)

@dp.message_handler(state=TestStates.TEST_STATE_2[0])
async def second_test_state_case_met(message: types.Message):
    await message.reply('Второй!', reply=False)

@dp.message_handler(state=TestStates.TEST_STATE_3 | TestStates.TEST_STATE_4)
async def third_or_fourth_test_state_case_met(message: types.Message):
    await message.reply('Третий или четвертый!', reply=False)

@dp.message_handler(state=TestStates.all())
async def some_test_state_case_met(message: types.Message):
    with dp.current_state(user=message.from_user.id) as state:
        text = MESSAGES['current_state'].format(
            current_state=await state.get_state(),
            states=TestStates.all()
        )
    await message.reply(text, reply=False)

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)



async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)