from aiogram import Router, types, Bot
from aiogram.types import CallbackQuery
from database.db import add_donation, get_total_donations
from utils.keyboards import currency_keyboard, country_keyboard
from config import GROUP_ID

router = Router()

# Временное хранилище валюты и страны для каждого пользователя
user_currency = {}
user_country = {}

# Шаг 1: Показываем пользователю выбор валюты
@router.callback_query(lambda callback: callback.data == "donate")
async def ask_for_currency(callback: CallbackQuery):
    await callback.message.answer("Пожалуйста, выберите валюту для пожертвования :", reply_markup=currency_keyboard())

# Шаг 2: Пользователь выбирает валюту
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
    await callback.message.answer(f"Вы выбрали валюту: {currency}. Теперь, выберите страну где находитесь:", reply_markup=country_keyboard())

# Шаг 3: Пользователь выбирает страну
@router.callback_query(lambda callback: callback.data.startswith("country_"))
async def choose_country(callback: CallbackQuery):
    # Извлекаем название страны из callback_data
    country = callback.data.replace("country_", "").capitalize()

    # Сохраняем страну для пользователя
    user_country[callback.from_user.id] = country
    await callback.message.answer(f"Вы выбрали страну: {country}. Пожалуйста, введите сумму для пожертвования:")


# Шаг 4: Получаем сумму пожертвования и записываем её с валютой и страной
@router.message()
async def receive_donation(message: types.Message, bot: Bot):
    user_id = message.from_user.id

    # Проверяем, что пользователь выбрал валюту и страну
    if not message.text:
        await message.answer("Пожалуйста, введите сумму пожертвования.")
        return

    if user_id not in user_currency or user_id not in user_country:
        await message.answer("Пожалуйста, завершите процесс, выбрав валюту и страну.")
        return

    try:
        amount = float(message.text)
        currency = user_currency[user_id]
        country = user_country[user_id]

        # Сохраняем пожертвование в базу данных
        await add_donation(user_id=user_id, amount=amount, currency=currency)

        # Получаем общую сумму пожертвований для данной валюты
        total_donations = await get_total_donations(currency)

        # Отправляем сообщение пользователю
        await message.answer(
            f"ДжазакаАллаху хайран за пожертвование в размере {amount} {currency} из {country}!\n"
            f"Общая сумма пожертвований в {currency}: {total_donations}.\n"
            f"С вами свяжутся через телеграм, будьте на связи"
        )

        # Формируем ссылку на профиль пользователя
        user_profile_link = f'<a href="tg://user?id={user_id}">{message.from_user.full_name}</a>'

        # Отправляем сообщение в группу
        group_message = (
            f"Новое пожертвование:\n"
            f"Пользователь: {user_profile_link}\n"
            f"Сумма: {amount} {currency}\n"
            f"Страна: {country}"
        )
        await bot.send_message(chat_id=GROUP_ID, text=group_message, parse_mode="HTML")

        # Удаляем данные о выбранной валюте и стране для пользователя
        del user_currency[user_id]
        del user_country[user_id]

    except ValueError:
        await message.answer("Пожалуйста, введите корректную сумму.")
