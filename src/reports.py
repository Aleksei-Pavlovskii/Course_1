from datetime import datetime

import pandas as pd


def spending_by_category(transactions: pd.DataFrame, category: str, date: str | None = None) -> pd.DataFrame:
    """
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    """
    if not date:
        date = datetime.today()
    else:
        date = pd.to_datetime(date, format="%Y-%m-%d %H:%M:%S")
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], dayfirst=True, format="%d.%m.%Y %H:%M:%S"
    )
    start_date = date - pd.DateOffset(months=3)
    filter_df = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
        & (transactions["Категория"] == category)
    ]

    return filter_df
