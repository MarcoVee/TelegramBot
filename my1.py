# !venv/bin/python
from aiogram import executor
from dispatcher import dp
import handlers

from db import BotDB
BotDB = BotDB("Databasa1.db")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
