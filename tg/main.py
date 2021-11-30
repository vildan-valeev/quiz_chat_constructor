import asyncio

import aiogram
from aiohttp import web

from bots_manager import Bots
from db_api import get_tokens

app = web.Application()
routes = web.RouteTableDef()
bot_manager = Bots()


@routes.post('/tgbot/{webhook}')
async def handle(request: web.Request) -> web.Response:
    """Получаем апдейты"""
    token = request.match_info["webhook"]

    bot = bot_manager.Bots.get(token)
    if not bot:
        return web.json_response(status=403)

    data = await request.json()
    # print(data)
    update = aiogram.types.Update(**data)
    print(update)
    await bot_manager.new_update(bot, update)
    return web.Response()  # status=200


@routes.post('/new-bot/')
async def handle(request: web.Request) -> web.Response:
    """Получаем новые токены для запуска бота"""
    token = None
    data = await request.json()
    print(data)
    # TODO: переписать условия проверки
    if 'token' in data:
        token = data['token']
    bot = bot_manager.Bots.get(token)
    if not bot:
        await bot_manager.add(token)
        bot = bot_manager.Bots.get(token)
        await bot.set_webhook()
    return web.Response(text='OK')  # status=200


@routes.post('/delete-bot/')
async def handle(request: web.Request) -> web.Response:
    """Удаляем бота..."""
    token = None
    data = await request.json()
    print(data)
    # TODO: переписать условия проверки
    if 'token' in data:
        token = data['token']
    bot = bot_manager.Bots.get(token)
    if bot:
        await bot.delete_webhook()
        await bot_manager.remove(token)
    return web.Response(text='OK')  # status=200


app.add_routes(routes)


async def start():
    bot_response = await get_tokens()
    for i in bot_response['results']:
        if i['tg_token'] is None:
            continue
        else:
            await bot_manager.add(i['tg_token'])
            bot = bot_manager.Bots.get(i['tg_token'])
            await bot.set_webhook()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    web.run_app(app, port=6000)
