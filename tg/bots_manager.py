from typing import AnyStr, Optional, Dict

import aiogram
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from answers import cmd_start, another_msg, add_name, result, category, service, staff, add_date, add_phone, cancel, \
    contacts
from config import DOMAIN
from state import Order


class TGBot(object):
    def __init__(self, token: AnyStr, host: Optional[AnyStr] = None) -> None:
        self.host = host if host else DOMAIN
        self.token = token
        self.bot: aiogram.Bot = aiogram.Bot(token)
        self.storage = MemoryStorage()
        self.dispatcher: Dispatcher = Dispatcher(self.bot, storage=self.storage)
        self.dispatcher.register_message_handler(callback=cmd_start, commands=["start", "help"], state='*')
        self.dispatcher.register_message_handler(callback=cancel, text='cancel', state='*')
        self.dispatcher.register_message_handler(callback=category, text_contains='Добавить заявку', state='*')
        self.dispatcher.register_message_handler(callback=contacts, text_contains='Контакты', state='*')
        self.dispatcher.register_callback_query_handler(callback=service, state=Order.S1)
        self.dispatcher.register_callback_query_handler(callback=staff, state=Order.S2)
        self.dispatcher.register_callback_query_handler(callback=add_date, state=Order.S3)
        self.dispatcher.register_message_handler(callback=add_name, state=Order.S4)
        self.dispatcher.register_message_handler(callback=add_phone, state=Order.S5)
        self.dispatcher.register_message_handler(callback=result, state=Order.S6)

        self.dispatcher.register_message_handler(callback=another_msg, state='*')
        # print(self.dispatcher.message_handlers)

    async def set_webhook(self):
        print(f'Установка вебхука {self.token}')
        await self.bot.set_webhook(f"{self.host}/tgbot/{self.token}")

    async def delete_webhook(self):
        print('Удаление вебхука')
        await self.bot.delete_webhook(drop_pending_updates=True)

    def __init_logger(self) -> None:
        pass
    # def __init_logger(self) -> None:
    #     loop = asyncio.get_event_loop()
    #     info: aiogram.types.User = loop.run_until_complete(self.bot.get_me())
    #     self.logger = logging.getLogger(info.username)


class Bots:
    def __init__(self):
        self.Bots: Dict[AnyStr, TGBot] = dict()
        self.count = 0

    async def add(self, token: AnyStr) -> None:
        if token in self.Bots:
            print(f'Error: bot with name {token} exist')
            return
        self.Bots[token] = TGBot(token=token)
        print(self.Bots)
        self.count += 1

    async def remove(self, token: AnyStr) -> None:
        if token not in self.Bots:
            print(f'Error: bot with name {token} doesnotexist')
            return
        self.Bots.pop(token)
        print(self.Bots)
        self.count -= 1

    def get_tg_bot(self, token: AnyStr) -> Optional[TGBot]:
        return self.Bots.get(token)

    async def new_update(self, tgbot: TGBot, update: aiogram.types.Update):
        print("запуск апдейтов в диспетчера")
        tgbot.bot.set_current(tgbot.bot)
        tgbot.dispatcher.set_current(tgbot.dispatcher)
        await tgbot.dispatcher.process_update(update)
        # tgbot.dispatcher.get_current().current_state()

