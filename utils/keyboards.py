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
