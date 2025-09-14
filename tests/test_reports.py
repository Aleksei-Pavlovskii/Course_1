import pandas as pd
from pandas import DataFrame

from src.reports import spending_by_category


def test_spending_by_category(table_xlsx: DataFrame) -> None:
    expected_result = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["03.12.2021 14:49:41"], dayfirst=True),
            "Дата платежа": ["03.12.2021"],
            "Номер карты": ["*4556"],
            "Сумма операции": [-200],
            "Кэшбэк": [2],
            "Категория": ["Дом и ремонт"],
            "Описание": ["Перекрёсток"],
            "Сумма операции с округлением": [200],
        }
    )

    result = spending_by_category(table_xlsx, "Дом и ремонт", "2021-12-03 14:49:41")
    result = result.reset_index(drop=True)
    expected_result = expected_result.reset_index(drop=True)
    pd.testing.assert_frame_equal(result, expected_result)


def test_spending_by_category_none_date(table_xlsx_2: DataFrame) -> None:
    expected_result = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["03.09.2025 14:49:41"], dayfirst=True),
            "Дата платежа": ["03.12.2021"],
            "Номер карты": ["*4556"],
            "Сумма операции": [-200],
            "Кэшбэк": [2],
            "Категория": ["Дом и ремонт"],
            "Описание": ["Перекрёсток"],
            "Сумма операции с округлением": [200],
        }
    )

    result = spending_by_category(table_xlsx_2, "Дом и ремонт")
    result = result.reset_index(drop=True)
    expected_result = expected_result.reset_index(drop=True)
    pd.testing.assert_frame_equal(result, expected_result)
