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


"""class ScriptStatus:
    is_command_name: bool = False
    is_command: bool = False
    is_message: bool = False
    is_change_value1: bool = False
    is_change_value2: bool = False
    is_start_command: int = 0

    command_name: str = str()
    message: str = str()
    change_value1: str = str()
    change_value2: str = str()


def loader(status_script: ScriptStatus, words: list[str]):
    for word in words:

        # Checking status
            
        if status_script.is_command_name:
            status_script.command_name = word

            status_script.is_command_name = False

        elif status_script.is_message:
            status_script.message = word
            status_script.is_message = False

        elif status_script.is_change_value1:
            status_script.change_value1 = '"' + word + '"'
            status_script.is_change_value1 = False

        elif status_script.is_change_value2:
            status_script.change_value2 = '"' + word+ '"'
            status_script.is_change_value2 = False

        # Checking word

        if 'COMMAND' in word:
            status_script.is_command_name = True

        elif 'CALLED' in word:
            status_script.is_command = True

        elif 'SEND MESSAGE' in word:
            status_script.is_message = True

        elif 'SET' in word:
            status_script.is_change_value1 = True

        elif 'VALUE' in word:
            status_script.is_change_value2 = True

        elif 'USER INPUT' in word:
            status_script.is_input_need = True

        elif 'END' in word:
            status_script.is_command = False"""
