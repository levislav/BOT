import asyncio
import time
from typing import Optional, Text

from aiogram import *

import db


class Timer:
    def __init__(self, bot: Bot, bot_dispatcher: Dispatcher):
        self.is_start = False
        self.task_time = Optional[str]
        self.bot = bot
        self.bot_dispatcher = bot_dispatcher

    async def set_time(self, task_time, message):
        self.task_time = task_time
        await db.update_db('timer', self.task_time,
                           message.chat.id)

    async def start(self, username, chat):
        self.is_start = True
        while self.is_start:
            if str(time.ctime(time.time()))[11:16] == self.task_time:
                await self.bot.send_message(chat,
                                            text=open(f"tasks\\{await db.get_db('department', chat)}", 'r', encoding='utf-8').read().split('\n\n')[await db.get_db('progress', chat)])
                await db.update_db("progress", str(int(await db.get_db("progress", chat)) + 1), chat)
                await asyncio.sleep(60)
            await asyncio.sleep(2)

    async def stop(self):
        self.is_start = False


async def user_input(bot_dispatcher: Dispatcher) -> str:
    global input_text
    input_text = None
    print('userinput:')
    while not input_text:

        @bot_dispatcher.message_handler()
        async def get_input(message):
            global input_text
            input_text = message.text
            print(input_text)

        await asyncio.sleep(0.5)

    print("user_input finished.")
    #bot_dispatcher = None
    return input_text


async def get_callback_data(bot_dispatcher: Dispatcher, user_id):
    callback_data = None

    @bot_dispatcher.callback_query_handler(user_id=user_id)
    async def check_callback_handlers(callback):
        nonlocal callback_data
        print(callback.data)
        callback_data = callback.data
        print(callback_data)
    return callback_data


