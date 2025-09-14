import json
from unittest.mock import Mock, patch

from pandas import DataFrame

from src.services import analyze_cashback


@patch("pandas.read_excel")
def test_analyze_cashback(mock_xlsx: Mock, table_xlsx: DataFrame) -> None:

    mock_xlsx.return_value = table_xlsx
    expected_dict = {"Местный транспорт": 34, "Супермаркеты": 44, "Дом и ремонт": 2}

    result_json = analyze_cashback("test_file.xlsx", 2021, 12)
    result_dict = json.loads(result_json)
    assert result_dict == expected_dict
