import pandas as pd
from unittest.mock import patch
import os

from src.decorators import write_reports_to_csv


def test_write_reports_to_csv():
    test_data = pd.DataFrame({'test': [1, 2, 3]})

    @write_reports_to_csv
    def mock_function():
        return test_data

    with patch('os.makedirs') as mock_makedirs:
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            result = mock_function()

            assert result.equals(test_data)
            mock_makedirs.assert_called_once_with('data', exist_ok=True)
            mock_to_csv.assert_called_once_with('data/reports.csv', index=False, encoding='utf-8-sig')