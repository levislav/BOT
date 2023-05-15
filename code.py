import sqlite3

import aiogram
import classes
import db
import intrepretator2


async def main(bot: aiogram.Bot, bot_dispatcher: aiogram.Dispatcher):
    @bot_dispatcher.message_handler(commands=['start'])
    async def start_bot(message):
        global timer
        db.connect_db()
        await bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}! Я Телеграм Бот для новых сотрудников GoMobile!\n"
                                                f"Чтобы продолжить, мне надо получить от тебя некоторую информацию.")

        kb = aiogram.types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
        b1 = aiogram.types.KeyboardButton("department1")
        b2 = aiogram.types.KeyboardButton("department2")
        kb.add(b1, b2)

        await bot.send_message(message.chat.id, "Во первых, в каком отделе ты работаешь?", reply_markup=kb)
        department = await classes.user_input(bot_dispatcher)

        await bot.send_message(message.chat.id, "Отлично!\n"
                                                "Каждый день я буду присылать тебе задания.\n"
                                                "Напиши, во сколько тебе удобно)\n"
                                                "Формат - ЧЧ:ММ")

        time = await classes.user_input(bot_dispatcher)

        while not(int(time[:1]) < 25 and time[2] == ':' and int(time[3:4]) <= 60):
            await bot.send_message(message.chat.id, "Похоже, что вы не так ввели время. Формат: ЧЧ:ММ \nПример: 09:20")
            time = await classes.user_input(bot_dispatcher)

        await bot.send_message(message.chat.id, "Готово! Будут вопросы - пиши сюда.\n"
                                                "Нужно будет изменить время, когда будет приходить задание - /timer\n"
                                                "Другие команды + информация о боте - /help\n\n"
                                                "Удачи!")

        timer = classes.Timer(bot=bot, bot_dispatcher=bot_dispatcher)
        await timer.set_time(time, message)
        await db.start_db([message.chat.id, time, department, 0])
        await timer.start(message.chat.first_name, message.chat.id)



    @bot_dispatcher.message_handler(commands=['help'])
    async def get_help(message):
        ...

    @bot_dispatcher.message_handler(commands=['timer'])
    async def set_timer(message):
        global timer
        await timer.stop()
        await bot.send_message(message.chat.id, "Во сколько мне надо присылать тебе задания?\n"
                                                "Формат: ЧЧ:ММ")

        time = await classes.user_input(bot_dispatcher)

        while not (int(time[:1]) < 25 and time[2] == ':' and int(time[3:4]) <= 60):
            await bot.send_message(message.chat.id, "Похоже, что вы не так ввели время. Формат: ЧЧ:ММ \nПример: 09:20")
            time = await classes.user_input(bot_dispatcher)

        await bot.send_message(message.chat.id, f"Готово! Теперь время будет приходить в {time}.")

        timer = classes.Timer(bot=bot, bot_dispatcher=bot_dispatcher)
        await timer.set_time(time, message)
        await db.update_db("timer", time, message.chat.id)
        await timer.start(message.chat.first_name, message.chat.id)

    @bot_dispatcher.message_handler(commands=['__stop_bot'])
    async def __stop_bot(message):
        raise SystemExit

    @bot_dispatcher.message_handler(commands=['__info'])
    async def __info(message):
        await bot.send_message(message.chat.id, message)


async def start():
    await main(bot=intrepretator2.bot, bot_dispatcher=intrepretator2.bot_dispatcher_main)

