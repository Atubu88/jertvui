from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime  # Импортируем класс datetime, а не модуль

Base = declarative_base()

class Donation(Base):
    __tablename__ = 'donations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)  # Поле для валюты
    timestamp = Column(DateTime, default=datetime.utcnow)  # Поле для