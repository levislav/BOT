from aiogram import *
import classes
import db
import settings


def scripter(bot_script, code_blank=settings.code_blank, pyscr=settings.python_script):
    # Creating object with information, which part of script is processed and with names, taken from script
    script_stats = classes.ScriptStatus()

    # Just reading files, nothing hard
    script = open(bot_script, 'r', encoding='utf-8').read()
    blank = open(code_blank, 'r', encoding='utf-8').read()

    result = str()

    with open(pyscr, 'w', encoding='utf-8') as pyscript:
        result += blank

        for command in script.split("\nEND\n\n"):
            for index, line in enumerate(command.split('\n')):

                # Now we should check if it is beginning of the command, cause there is a bit of different syntax
                spliting_symbol = ' - ' if index else ' '
                classes.loader(script_stats, line.split(spliting_symbol))
                if script_stats.command_name:
                    result += f"""
    @bot_dispatcher.message_handler(commands=[\'{script_stats.command_name}\'])
    async def {script_stats.command_name}(message):
        global encoder_dict
        await db.start_db(([str([message.from_user.id,
                 message.from_user.first_name,
                 message.from_user.last_name,
                 message.from_user.username]),
            str(),
            str(),
            str(),
            0]))
           
    """
                    script_stats.command_name = None
                elif script_stats.is_command:
                    if script_stats.message:
                        result += f"""
        await bot.send_message(message.chat.id, \'{script_stats.message}\'.translate(encoder_dict))
"""
                        script_stats.message = None

                    elif script_stats.change_value1:
                        if script_stats.change_value2 == '"USER INPUT"':
                            script_stats.change_value2 = 'await classes.user_input(bot_dispatcher, message.chat.id)'
                        if script_stats.change_value1 in db.structure:
                            result += f"""
        await db.update_db(\'{script_stats.change_value1}\', {script_stats.change_value2},
                            str([message.from_user.id,
                                 message.from_user.first_name,
                                 message.from_user.last_name,
                                 message.from_user.username])"""

                        else:
                            result += f"""
        encoder_dict[{'{' + script_stats.change_value1 + '}'}] = {script_stats.change_value2}"""

    result += """

async def start():
    await main(bot=intrepretator2.bot, bot_dispatcher=intrepretator2.bot_dispatcher_main)
                    """
    return result

bot = Bot(token=settings.token)
bot_dispatcher_main = Dispatcher(bot)


def start():
    with open("code.py", 'w', encoding='utf-8') as f:
        f.write(scripter(settings.telegram_script))
