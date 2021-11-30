from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

btn_cancel = InlineKeyboardButton(text="Отмена", callback_data='cancel')


async def get_category_menu(data):
    menu = InlineKeyboardMarkup(row_width=1)
    for i in data['categories']:
        menu.insert(InlineKeyboardButton(text=f"{i['title']}", callback_data=f'category-{i["id"]}'))
    menu.add(btn_cancel)

    return menu


async def get_service_menu(category: str, constructor):
    menu = InlineKeyboardMarkup(row_width=1)
    cat_id = category.split('-')
    for i in constructor['categories']:
        print(i)
        if int(cat_id[-1]) == i['id']:
            for sr in i['service']:
                menu.insert(InlineKeyboardButton(text=f"{sr['name']}", callback_data=f'service-{sr["id"]}'))
    menu.add(btn_cancel)

    return menu


async def get_staff_menu(category: str, service: str, constructor):
    menu = InlineKeyboardMarkup(row_width=1)
    cat_id = category.split('-')
    service_id = service.split('-')
    for i in constructor['categories']:
        print(i)
        if int(cat_id[-1]) == i['id']:
            for sr in i['service']:
                if int(service_id[-1]) == sr['id']:
                    for st in sr['staff']:
                        menu.insert(InlineKeyboardButton(text=f"{st['name']}", callback_data=f'staff-{st["id"]}'))
    menu.add(btn_cancel)
    return menu


contacts = KeyboardButton(text=f"Контакты")
add_btn = KeyboardButton(text=f"Добавить заявку")
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(add_btn, contacts)
