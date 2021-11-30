from aiohttp import web

from colorz import get_color

app = web.Application()
routes = web.RouteTableDef()


@routes.post('/')
async def webhook(request):
    data = await request.post()
    # print(data)
    # print(bot.get_updates())
    file = data['file'].file

    answer = get_color(file)
    data = {'colors': answer}
    return web.json_response(data, status=200)


app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=7500)
