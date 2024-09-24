# Указываем базовый образ с установленным Python 3.11
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей (requirements.txt) в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код бота в контейнер
COPY . .

# Указываем volume для сохранения данных (опционально)
VOLUME ["/app"]

# Указываем команду для запуска бота
CMD ["python", "main.py"]
