from unittest.mock import MagicMock, Mock, mock_open, patch

import pandas as pd
from pandas import DataFrame

from src.utils import (get_card_with_spend, get_currency, get_data_time, get_slice_period, get_stock,
                       get_top_transactions, get_user_time)


@patch("src.utils.datetime")
def test_get_user_time_morning(mock_datetime: Mock) -> None:
    mock_now = Mock()
    mock_now.hour = 9
    mock_datetime.now.return_value = mock_now
    assert get_user_time() == "Доброе утро"


@patch("src.utils.datetime")
def test_get_user_time_day(mock_datetime: Mock) -> None:
    mock_now = Mock()
    mock_now.hour = 14
    mock_datetime.now.return_value = mock_now
    assert get_user_time() == "Добрый день"


@patch("src.utils.datetime")
def test_get_user_time_evening(mock_datetime: Mock) -> None:
    mock_now = Mock()
    mock_now.hour = 20
    mock_datetime.now.return_value = mock_now
    assert get_user_time() == "Добрый вечер"


@patch("src.utils.datetime")
def test_get_user_time_night(mock_datetime: Mock) -> None:
    mock_now = Mock()
    mock_now.hour = 1
    mock_datetime.now.return_value = mock_now
    assert get_user_time() == "Доброй ночи"


def test_get_data_time() -> None:
    assert get_data_time("2018-05-05 15:30:00") == ["01.05.2018 15:30:00", "05.05.2018 15:30:00"]


@patch("pandas.read_excel")
def test_get_slice_period(mock_xlsx: Mock, table_xlsx: DataFrame, period: list) -> None:
    mock_xlsx.return_value = table_xlsx
    result_df = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["01.12.2021 13:12:18", "02.12.2021 14:41:17"], dayfirst=True),
            "Дата платежа": ["01.12.2021", "02.12.2021"],
            "Номер карты": ["*7197", "*5091"],
            "Сумма операции": [-3499, -4451],
            "Кэшбэк": [34, 44],
            "Категория": ["Местный транспорт", "Супермаркеты"],
            "Описание": ["Хлеб", "Улыбка радуги"],
            "Сумма операции с округлением": [3499, 4451],
        }
    )
    result = get_slice_period("test_file.xlsx", period)
    result = result.reset_index(drop=True)
    result_df = result_df.reset_index(drop=True)
    pd.testing.assert_frame_equal(result, result_df)


@patch("pandas.read_excel")
def test_get_card_with_spend(table_xlsx: DataFrame) -> None:
    df = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["01.12.2021 13:12:18", "02.12.2021 14:41:17"], dayfirst=True),
            "Дата платежа": ["01.12.2021", "02.12.2021"],
            "Номер карты": ["*7197", "*5091"],
            "Сумма операции": [-3499, -4451],
            "Кэшбэк": [34, 44],
            "Категория": ["Местный транспорт", "Супермаркеты"],
            "Описание": ["Хлеб", "Улыбка радуги"],
            "Сумма операции с округлением": [3499, 4451],
        }
    )
    result_card = [
        {"last_digits": "7197", "total_spent": 3499, "cashback": 34},
        {"last_digits": "5091", "total_spent": 4451, "cashback": 44},
    ]
    assert get_card_with_spend(df) == result_card


def test_get_top_transactions(table_xlsx: DataFrame) -> None:
    result_top_transactions = [
        {"date": "02.12.2021", "amount": "-4451", "category": "Супермаркеты", "description": "Улыбка радуги"},
        {"date": "01.12.2021", "amount": "-3499", "category": "Местный транспорт", "description": "Хлеб"},
    ]
    assert get_top_transactions(table_xlsx, 2) == result_top_transactions


@patch("src.utils.requests.request")
@patch("src.utils.os.path.exists")
@patch("src.utils.json.load")
@patch("builtins.open", new_callable=mock_open)
def test_get_currency(mock_open_file: Mock, mock_json_load: Mock, mock_os: Mock, r_mock: Mock) -> None:
    mock_os.return_value = True
    mock_json_load.return_value = {"user_currencies": ["USD"]}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"query": {"from": "USD"}, "result": 84.5}
    r_mock.return_value = mock_response
    expected_result = [{"currency": "USD", "rate": "84.5"}]
    result = get_currency("test.json")
    assert result == expected_result


@patch("src.utils.TDClient")
@patch("src.utils.os.path.exists")
@patch("src.utils.json.load")
@patch("builtins.open", new_callable=mock_open)
def test_get_stock(mock_open_file: Mock, mock_json_load: Mock, mock_os: Mock, mock_td_client: Mock) -> None:
    mock_os.return_value = True
    mock_json_load.return_value = {"user_stocks": ["AAPL"]}
    mock_td_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.as_json.return_value = {"price": 150.12, "symbol": "AAPL"}
    mock_td_instance.price.return_value = mock_response
    mock_td_client.return_value = mock_td_instance
    expected_result = [{"stock": "AAPL", "price": "150.12"}]
    result = get_stock("test.json")
    assert result == expected_result
