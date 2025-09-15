import json
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame
from twelvedata import TDClient
import logging

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

load_dotenv()

URL = "https://api.apilayer.com/exchangerates_data/convert"
token_api = os.getenv("API_KEY")
token_api_stock = os.getenv("API_KEY_STOCKS")


def get_user_time() -> str:
    """
    Функция возвращает «Доброе утро» / «Добрый день» / «Добрый вечер»
    / «Доброй ночи» в зависимости от текущего времени.
    """
    user_data_hour = datetime.now().hour
    logger.info(f"Время входа пользователя: {user_data_hour}")
    if 5 <= user_data_hour < 11:
        return "Доброе утро"
    elif 11 <= user_data_hour < 17:
        return "Добрый день"
    elif 17 <= user_data_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_data_time(data_time: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> list:
    """
    Функция, которая принимает дату пользователя и выдает список с начала месяца до указанной даты
    """
    dt = datetime.strptime(data_time, date_format)
    first_day_month = dt.replace(day=1)
    return [first_day_month.strftime("%d.%m.%Y %H:%M:%S"), dt.strftime("%d.%m.%Y %H:%M:%S")]


def get_slice_period(path: str, period_date: list) -> DataFrame:
    """
    Функция принимает путь к Excel файлу и список из начала и конца периода,
    и возвращает таблицу в заданном периоде
    """
    df = pd.read_excel(path)

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    start_date = datetime.strptime(period_date[0], "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(period_date[1], "%d.%m.%Y %H:%M:%S")
    logger.info(f'Выбран период с {start_date} по {end_date}')

    filter_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    sorted_df = filter_df.sort_values(by="Дата операции")
    return sorted_df


def get_card_with_spend(sort_df: DataFrame) -> list[dict]:
    """
    Функция принимает таблицу за определенный период и возвращает список карт с расходами
    """
    card_spent_transaction = []
    card_sorted = sort_df[["Номер карты", "Сумма операции", "Кэшбэк", "Сумма операции с округлением"]]
    for i, row in card_sorted.iterrows():
        if row["Сумма операции"] < 0:
            last_digits = str(row["Номер карты"]).replace("*", "")
            total_spent = row["Сумма операции с округлением"]
            cashback = total_spent // 100
            row = {"last_digits": last_digits, "total_spent": total_spent, "cashback": cashback}
            card_spent_transaction.append(row)

    return card_spent_transaction


def get_top_transactions(sort_df: DataFrame, get_top: int) -> list[dict]:
    """
    Функция принимает таблицу за определенный период и возвращает топ транзакций по сумме платежа
    """
    top_pay_transacions = []
    sorted_pay_df = sort_df.sort_values(by="Сумма операции")
    top_transacions = sorted_pay_df.head(get_top)
    top_transacions_sorted = top_transacions[["Дата платежа", "Сумма операции", "Категория", "Описание"]]
    for i, row in top_transacions_sorted.iterrows():
        transaction = {
            "date": f"{row["Дата платежа"]}",
            "amount": f"{row["Сумма операции"]}",
            "category": f"{row["Категория"]}",
            "description": f"{row["Описание"]}",
        }
        top_pay_transacions.append(transaction)

    return top_pay_transacions


def get_currency(path_to_json: str) -> list[dict]:
    """
    Функция принимает на вход путь до json файла и возвращает курс валют
    """
    currensy_rates = []
    with open(path_to_json, encoding="utf-8") as file:
        data = json.load(file)
        currences = data["user_currencies"]

        for currence in currences:
            params = {"amount": "1", "from": f"{currence}", "to": "RUB"}
            headers = {"apikey": token_api}
            response = requests.request("GET", URL, headers=headers, params=params)
            status_code = response.status_code
            if status_code == 200:
                result = response.json()
                currency_code_response = result["query"]["from"]
                currency_amount = round(result["result"], 2)
                currensy_rates.append({"currency": f"{currency_code_response}", "rate": f"{currency_amount}"})
    return currensy_rates


def get_stock(path_to_json: str) -> list[dict]:
    """
    Функция принимает на вход path_to_json и возвращает курс акций
    """
    stock_rates = []
    with open(path_to_json, encoding="utf-8") as file:
        data = json.load(file)
        stocks = data["user_stocks"]

        td = TDClient(apikey=token_api_stock)

        for stock in stocks:
            price = td.price(symbol=stock).as_json()
            stock_rates.append({"stock": stock, "price": f"{round(float(price["price"]), 2)}"})
        return stock_rates


def read_xlsx(path: str) -> DataFrame:
    data = pd.read_excel(path)
    return data
