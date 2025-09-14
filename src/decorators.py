from functools import wraps
from typing import Any, Callable


def write_reports_to_csv(func: Callable) -> Any:
    """Декоратор для записи отчёта в CSV файл"""

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> Any:
        result = func(*args, **kwargs)
        result.to_csv('data/reports.csv', index=False, encoding='utf-8-sig')
        return result
    return wrapper
