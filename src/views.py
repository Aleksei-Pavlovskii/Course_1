import json

from src.utils import (get_card_with_spend, get_currency, get_data_time, get_slice_period, get_stock,
                       get_top_transactions, get_user_time)


def main_info(data_time: str) -> str:
    """
    Функция, принимающая на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ
    :param data_time:
    :return:
    """
    # Делаем срез всего экселя на определенный диапозон
    period = get_data_time(data_time)
    sort_df = get_slice_period("data/operations.xlsx", period)

    # 1. Привествие
    greeting = get_user_time()

    # 2. По каждой карте
    cards = get_card_with_spend(sort_df)

    # 3. Топ 5 транзакций
    top_transactions = get_top_transactions(sort_df, 5)

    # 4. Курс валют
    currency_rates = get_currency("data/user_settings.json")

    # 5. Стоимость акций из S&P500
    stock_prices = get_stock("data/user_settings.json")

    data = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    return json_data
