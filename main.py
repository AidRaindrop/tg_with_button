from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
#from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from cred import *
from testAPI import getcourse as getcourse
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.utils.emoji import emojize
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import emoji
import logging
import sqlite3

import asyncio
import logging

#API_TOKEN = TOKEN
#ADMIN = ADMIN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


BASE_MEDIA_PATH = './demo-media'
CAT_BIG_EYES = BASE_MEDIA_PATH+'/pics/'+'kitten0.jpg'
KITTENS = [
    open(BASE_MEDIA_PATH+'/pics/'+'kitten1.jpg', 'rb'),
    open(BASE_MEDIA_PATH+'/pics/'+'kitten2.jpg', 'rb'),
    open(BASE_MEDIA_PATH+'/pics/'+'kitten3.jpg', 'rb')
]
VOICE = open(BASE_MEDIA_PATH+"/ogg/"+"Rick_Astley_-_Never_Gonna_Give_You_Up.ogg", 'rb')
VIDEO = open(BASE_MEDIA_PATH+'/videos/'+'hedgehog.mp4', 'rb')
TEXT_FILE = open(BASE_MEDIA_PATH+'/files/'+'very important text file.txt', 'rb')
VIDEO_NOTE = open(BASE_MEDIA_PATH+'/videoNotes/'+'cute-puppy.mp4', 'rb')
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text(bold('Я могу ответить на следующие команды:'),
               '/voice', '/photo', '/group', '/note', '/file', '/testpre', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)



@dp.message_handler(commands=['course'])
async def echo_message(msg: types.Message):
    course = getcourse()
    #print('hellofff')
    await bot.send_message(msg.from_user.id, course)

@dp.message_handler(commands=['ping'])
async def echo_message(msg: types.Message):
    await msg.answer("напиши мне адрес для пинга")

    #async def gettextatclients(user_id, text):
        #await
    ip=msg.text
    ping = getcourse(ip)
    #print('hellofff')
    await bot.send_message(msg.from_user.id, course)

@dp.message_handler(commands=['voice'])
async def process_voice_command(message: types.Message):
    await bot.send_voice(message.from_user.id, VOICE,
                         reply_to_message_id=message.message_id)

@dp.message_handler(commands=['photo'])
async def process_photo_command(message: types.Message):
    caption = 'Какие глазки! :eyes:'
    await bot.send_photo(message.from_user.id, CAT_BIG_EYES,
                         caption=emojize(caption),
                         reply_to_message_id=message.message_id)

@dp.message_handler(commands=['group'])
async def process_group_command(message: types.Message):
    media = [InputMediaVideo(VIDEO, 'ёжик и котятки')]
    for photo_id in KITTENS:
        media.append(InputMediaPhoto(photo_id))
    await bot.send_media_group(message.from_user.id, media)

@dp.message_handler(commands=['note'])
async def process_note_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.RECORD_VIDEO_NOTE)
    await asyncio.sleep(1)  # конвертируем видео и отправляем его пользователю
    await bot.send_video_note(message.from_user.id, VIDEO_NOTE)

@dp.message_handler(commands=['file'])
async def process_file_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.UPLOAD_DOCUMENT)
    await asyncio.sleep(1)  # скачиваем файл и отправляем его пользователю
    await bot.send_document(user_id, TEXT_FILE,
                            caption='Этот файл специально для тебя!')

@dp.message_handler(commands=['testpre'])
async def process_testpre_command(message: types.Message):
    message_text = pre(emojize('''@dp.message_handler(commands=['testpre'])
    async def process_testpre_command(message: types.Message):
    message_text = pre(emojize('Ха! Не в этот раз :smirk:'))
    await bot.send_message(message.from_user.id, message_text)'''))
    await bot.send_message(message.from_user.id, message_text,
                           parse_mode=ParseMode.MARKDOWN)

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)

@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text(emojize('Я не знаю, что с этим делать :astonished:'),
                        italic('\nЯ просто напомню,'), 'что есть',
                        code('команда'), '/help')
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp)