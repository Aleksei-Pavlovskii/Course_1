import json
from unittest.mock import Mock, patch

import pandas

from src.views import main_info


@patch("src.views.get_stock")
@patch("src.views.get_currency")
@patch("src.views.get_top_transactions")
@patch("src.views.get_card_with_spend")
@patch("src.views.get_user_time")
@patch("src.views.get_slice_period")
@patch("src.views.get_data_time")
def test_main_info(
    mock_data: Mock,
    mock_data_period: Mock,
    mock_time: Mock,
    mock_card: Mock,
    mock_transactions: Mock,
    mock_currency: Mock,
    mock_stock: Mock,
) -> None:
    mock_data.return_value = ["01.12.2021 13:12:18", "02.12.2021 14:41:17"]
    mock_data_period.return_value = pandas.DataFrame(
        {
            "Дата операции": pandas.to_datetime(["01.12.2021 13:12:18", "02.12.2021 14:41:17"], dayfirst=True),
            "Дата платежа": ["01.12.2021", "02.12.2021"],
            "Номер карты": ["*7197", "*5091"],
            "Сумма операции": [-3499, -4451],
            "Кэшбэк": [34, 44],
            "Категория": ["Местный транспорт", "Супермаркеты"],
            "Описание": ["Хлеб", "Улыбка радуги"],
            "Сумма операции с округлением": [3499, 4451],
        }
    )
    mock_time.return_value = "Доброе утро"
    mock_card.return_value = [
        {"last_digits": "7197", "total_spent": 3499, "cashback": 34},
        {"last_digits": "5091", "total_spent": 4451, "cashback": 44},
    ]
    mock_transactions.return_value = [
        {"date": "02.12.2021", "amount": "-4451", "category": "Супермаркеты", "description": "Улыбка радуги"},
        {"date": "01.12.2021", "amount": "-3499", "category": "Местный транспорт", "description": "Хлеб"},
    ]
    mock_currency.return_value = [{"currency": "USD", "rate": "84.5"}]
    mock_stock.return_value = [{"stock": "AAPL", "price": "150.12"}]
    result = main_info("02.12.2021 14:41:17")

    expected_dict = {
        "greeting": "Доброе утро",
        "cards": [
            {"last_digits": "7197", "total_spent": 3499, "cashback": 34},
            {"last_digits": "5091", "total_spent": 4451, "cashback": 44},
        ],
        "top_transactions": [
            {"date": "02.12.2021", "amount": "-4451", "category": "Супермаркеты", "description": "Улыбка радуги"},
            {"date": "01.12.2021", "amount": "-3499", "category": "Местный транспорт", "description": "Хлеб"},
        ],
        "currency_rates": [{"currency": "USD", "rate": "84.5"}],
        "stock_prices": [{"stock": "AAPL", "price": "150.12"}],
    }

    # Преобразуем ожидаемый результат в JSON строку для сравнения
    expected_json = json.dumps(expected_dict, ensure_ascii=False, indent=4)

    assert result == expected_json
