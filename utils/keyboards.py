from aiogram.utils.keyboard import InlineKeyboardBuilder

def donate_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Пожертвовать", callback_data="donate")
    keyboard.button(text="Информация", callback_data="info")
    keyboard.button(text="Отчет", callback_data="report")
    return keyboard.as_markup()

def currency_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Доллары", callback_data="currency_usd")
    keyboard.button(text="Евро", callback_data="currency_eur")
    keyboard.button(text="Рубли", callback_data="currency_rub")
    keyboard.button(text="Гривны", callback_data="currency_uah")
    return keyboard.as_markup()


def country_keyboard():
    keyboard = InlineKeyboardBuilder()

    # Добавляем кнопки для стран. Каждая кнопка будет в своей строке.
    keyboard.button(text="США", callback_data="country_usa")
    keyboard.button(text="Германия", callback_data="country_germany")
    keyboard.button(text="Украина", callback_data="country_ukraine")
    keyboard.button(text="Швеция", callback_data="country_sweden")
    keyboard.button(text="Ирландия", callback_data="country_ireland")
    keyboard.button(text="Нидерланды", callback_data="country_netherlands")

    # Указываем, что каждая кнопка в отдельной строке
    return keyboard.adjust(2).as_markup()