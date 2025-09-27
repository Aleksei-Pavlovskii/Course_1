import json

import pandas as pd
import logging

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/services.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def analyze_cashback(file_path: str, year: int, month: int) -> str:
    """
    Анализирует выгодные категории кэшбэка и возвращает json строку с выгодными категориями кэшбэка
    """
    logger.info(f" Пользователь ввёл {year} год, {month} месяц")
    df = pd.read_excel(file_path)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filtered_data = df[
        (df["Дата операции"].dt.year == year) & (df["Дата операции"].dt.month == month) & (df["Кэшбэк"] > 0)
    ]

    expenses_by_category = filtered_data.groupby("Категория")["Кэшбэк"].sum()

    data = {}
    for i, row in expenses_by_category.items():
        data[i] = row
    logger.info(f"выгодные категории кэшбэка {data}")
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    return json_data
