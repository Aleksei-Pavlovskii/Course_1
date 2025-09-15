from functools import wraps
from typing import Any, Callable

import os


def write_reports_to_csv(func: Callable) -> Any:
    """
    Декоратор, который записывает отчет в CSV файл
    """
    def wrapper(*args: tuple, **kwargs: dict):
        result = func(*args, **kwargs)
        os.makedirs('data', exist_ok=True)
        result.to_csv('data/reports.csv', index=False, encoding='utf-8-sig')
        return result
    return wrapper
