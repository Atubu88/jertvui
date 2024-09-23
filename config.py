import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

# Получаем значения переменных
API_TOKEN = os.getenv('API_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')

