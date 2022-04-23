from aiogram import types
from dispatcher import dp
import config
import re
from my1 import BotDB


@dp.message_handler(commands="start")
async def start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id,):
        BotDB.add_user(message.from_user.id,)

    await message.bot.send_message(message.from_user.id, "Welcome!")


@dp.message_handler(commands=("spent", "s", "earned", "e"), commands_prefix="/!")
async def start(message: types.Message):
    cmd_variants = (('/spent', '/s', '!spent', '!s'), ('/earned', '/e', '!earned', '!e'))
    operation = "-" if message.text.startswith(cmd_variants[0]) else '+'

    value = message.text
    for i in cmd_variants:
        for j in i:
            value = value.replace(j, '').strip()

    if len(value):
        x = re.findall(r"\d+(?:.\d+)?", value)

        if len(x):
            value = float(x[0].replace(',', '.'))

            BotDB.add_record(message.from_user.id, operation, value)

            if operation == "-":
                await message.reply('Expense <u><b>record</b><u/> successfully entered!')
            else:
                await message.reply('Expense <u><b>income</b><u/> successfully entered!')

        else:
            await message.reply("Can't understand a somma")
    else:
        await message.reply('Write a somma again!')


@dp.message_handler(commands=("history", "h"), commands_prefix="/!")
async def start(message: types.Message):
    cmd_variants = ('/history', '/h', '!history', '!h')
    within_als = {
        "day": ('today', 'day', 'сегодня', 'день'),
        "month": ('month', 'месяц'),
        "year": ('year', 'год'),
    }

    cmd = message.text
    for r in cmd_variants:
        cmd = cmd.replace(r, '').strip()

    within = "day"
    if len(cmd):
        for k in within_als:
            for als in within_als[k]:
                if als == cmd:
                    within = k

    records = BotDB.get_records(message.from_user.id, within)

    if len(records):
        answer = f"🕘 Transaction history for {within_als[within][-1]}\n\n"

        for r in records:
            answer += "<b>" + ("➖ Consumption"if not r[2] else "➕ Income") + "</b>"
            answer += f" - {r[3]}"
            answer += f" <i> ({r[4]})</i>\n"

            await message.reply(answer)
    else:
        await message.reply("No entries found!")
