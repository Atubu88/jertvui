from aiogram import Router, types
from aiogram.types import CallbackQuery
from database.db import get_donations_report, get_total_donations_by_currency
from datetime import datetime

router = Router()

@router.callback_query(lambda callback: callback.data == "report")
async def send_report(callback: CallbackQuery):
    donations = await get_donations_report()

    if donations:
        report = "Отчет о пожертвованиях:\n\n"
        totals = {"USD": 0, "EUR": 0, "RUB": 0, "UAH": 0}

        user_count = 1  # Счётчик для пользователей

        for donation in donations:
            # Форматируем время пожертвования
            timestamp = donation.timestamp.strftime('%Y-%m-%d %H:%M:%S')

            # Заполняем отчет по каждому пожертвованию
            report += (f"{user_count} Садака, Сумма: {donation.amount} {donation.currency}, "
                       f"Дата и время: {timestamp}\n")
            totals[donation.currency] += donation.amount
            user_count += 1  # Увеличиваем счётчик пользователей

        # Добавляем итоговую информацию по каждой валюте
        report += "\nИтоговые суммы по валютам:\n"
        for currency, total in totals.items():
            report += f"{currency}: {total}\n"
    else:
        report = "На данный момент пожертвований нет."

    await callback.message.answer(report)
