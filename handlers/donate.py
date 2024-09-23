from aiogram import Router, types, Bot
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from database.db import add_donation, get_total_donations
from utils.keyboards import currency_keyboard
from config import GROUP_ID

router = Router()

# Временное хранилище валюты для каждого пользователя
user_currency = {}


# Шаг 1: Показываем пользователю выбор валюты
@router.callback_query(lambda callback: callback.data == "donate")
async def ask_for_currency(callback: CallbackQuery):

    await callback.message.answer("Пожалуйста, выберите валюту:", reply_markup=currency_keyboard())

# Пользователь выбирает валюту
@router.callback_query(lambda callback: callback.data.startswith("currency_"))
async def choose_currency(callback: CallbackQuery):
    currency_map = {
        "currency_usd": "USD",
        "currency_eur": "EUR",
        "currency_rub": "RUB",
        "currency_uah": "UAH"
    }
    currency = currency_map[callback.data]
    user_currency[callback.from_user.id] = currency
    await callback.message.answer(f"Вы выбрали валюту: {currency}. Пожалуйста, введите сумму для пожертвования:")


# Шаг 3: Получаем сумму пожертвования и записываем её с валютой
@router.message()
async def receive_donation(message: types.Message, bot: Bot):
    user_id = message.from_user.id

    # Проверка, что сообщение содержит текст
    if not message.text:
        await message.answer("Пожалуйста, введите сумму пожертвования.")
        return

    if user_id not in user_currency:
        await message.answer("Пожалуйста, сначала выберите валюту, используя команду /start.")
        return

    try:
        amount = float(message.text)

        currency = user_currency[user_id]

        # Сохраняем пожертвование в базу данных
        await add_donation(user_id=user_id, amount=amount, currency=currency)

        # Получаем общую сумму пожертвований для данной валюты
        total_donations = await get_total_donations(currency)

        # Отправляем сообщение пользователю
        await message.answer(
            f"ДжазакаАллаху хайран за пожертвование в размере {amount} {currency}!\n"
            f"Общая сумма в {currency}: {total_donations}.\n"
    
            "Скоро ин ша Аллах с вами свяжутся ."
        )

        # Формируем ссылку на профиль пользователя
        user_profile_link = f'<a href="tg://user?id={user_id}">{message.from_user.full_name}</a>'

        # Формируем сообщение для отправки в группу
        group_message = (f"Новое пожертвование:\n"
                         f"Пользователь: {user_profile_link}\n"
                         f"Сумма: {amount} {currency}")

        print(f"Sending message to group: {group_message}")

        # Отправляем сообщение в группу
        await bot.send_message(chat_id=GROUP_ID, text=group_message, parse_mode="HTML")

        # Удаляем данные о выбранной валюте для пользователя
        del user_currency[user_id]

    except ValueError:
        await message.answer("Пожалуйста, введите корректную сумму.")
