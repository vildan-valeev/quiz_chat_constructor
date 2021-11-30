import requests
import datetime
from config import BACKEND_URL


async def get_db_message(text_id, token):
    result = requests.get(f'{BACKEND_URL}/api/constructor/bottext/{text_id}/{token}/')
    data = result.json()
    # TODO: реализовать обработку ошибок в запросах
    return data['text']


async def get_tokens():
    """Получаем токены для запуска"""

    url = f"{BACKEND_URL}/api/auth/token/login/"

    payload = {'password': '25658545',
               'email': 'vvv@vvv.ru'}

    response = requests.post(url, data=payload)  # получаем токен авторизации

    url = f"{BACKEND_URL}/api/auth/users/"
    data = response.json()
    headers = {
        'Authorization': f"Token {data['auth_token']}"
    }
    # TODO: реализовать обработку ошибок в запросах
    response = requests.get(url=url, headers=headers)  # получаем конструкторы
    print(response.json())
    return response.json()


async def get_constructor_by_token(token):
    result = requests.get(f'{BACKEND_URL}/api/constructor/detail/{token}/')
    return result.json()


async def create_event(data):
    url = f"{BACKEND_URL}/api/constructor/event/"
    print(data)
    # TODO: реализовать обработку ошибок в запросах
    staff_id: str = data['staff']
    start = datetime.datetime.now()
    end = start + datetime.timedelta(hours=1)
    print(start, end)
    payload = {'staff': int(staff_id.split('-')[-1]),
               'start': start.strftime('%Y-%m-%dT%H:%M:%-S%Z'),
               'end': end.strftime('%Y-%m-%dT%H:%M:%-S%Z'),
               'phone': data['phone'],
               'name': data['name'],
               'status': 'BS',
               'details': f"Name: {data['name']}\n"
                          f"Phone:{data['phone']}\n"
                          f"Duration:\n"
                          f"Price: \n",

               }

    response = requests.post(url, data=payload)  # получаем токен авторизации
    print(response.status_code, response.text)
    if response.status_code == 201:
        return 'Заявка создана'
    return "Ошибка сервера"
