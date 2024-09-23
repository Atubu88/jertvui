import json
import os
from aiogram import Router, types
from aiogram.filters import CommandStart
from utils.keyboards import donate_keyboard  # Импортируем функцию с клавиатурой

router = Router()

# Путь к файлу для хранения списка авторизованных пользователей
AUTHORIZED_USERS_FILE = "authorized_users.json"

@router.message(CommandStart())
async def start_command(message: types.Message, command: CommandStart):
    user_id = message.from_user.id

    # Загрузка списка авторизованных пользователей из файла
    if os.path.exists(AUTHORIZED_USERS_FILE):
        with open(AUTHORIZED_USERS_FILE, "r") as file:
            authorized_users = json.load(file)
    else:
        authorized_users = []

    # Если пользователь уже авторизован, показываем клавиатуру с действиями
    if user_id in authorized_users:
        await message.answer("Ассалам уалекум братья, прежде всего ознакомьтесь инфой о боте", reply_markup=donate_keyboard())
        return

    # Получаем параметр из ссылки (например, invite_code)
    invite_code = command.args  # Параметр, переданный через ссылку

    # Если пользователь зашел без параметра (без ссылки)
    if not invite_code:
        await message.answer("Для доступа к боту требуется пригласительная ссылка.")
        return

    # Проверяем корректность приглашения (invite_code)
    if invite_code == "invite_code":  # Проверка на корректный код
        authorized_users.append(user_id)  # Добавляем пользователя в список авторизованных

        # Сохранение обновленного списка в файл
        with open(AUTHORIZED_USERS_FILE, "w") as file:
            json.dump(authorized_users, file)

        await message.answer("Авторизация прошла успешно! Вы можете пользоваться ботом.", reply_markup=donate_keyboard())
    else:
        await message.answer("Неверный код приглашения. Доступ запрещён.")
