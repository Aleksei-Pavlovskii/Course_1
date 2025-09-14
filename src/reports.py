from datetime import datetime

import pandas as pd
import logging

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/reports.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def spending_by_category(transactions: pd.DataFrame, category: str, date: str | None = None) -> pd.DataFrame:
    """
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    """
    logger.info(f"Выбрана категория {category}")
    if not date:
        date = datetime.today()
        logger.info("Пользователь запросил данные за последние 3 месяца")
    else:
        date = pd.to_datetime(date, format="%Y-%m-%d %H:%M:%S")
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], dayfirst=True, format="%d.%m.%Y %H:%M:%S"
    )
    start_date = date - pd.DateOffset(months=3)
    logger.info(f"Пользователь запросил данные с {start_date} по {date}")
    filter_df = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
        & (transactions["Категория"] == category)
    ]

    return filter_df
