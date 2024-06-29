import json
import logging
import re
from typing import Any, Dict, List

import pandas as pd

from src.utils import ligging_setup

logger = ligging_setup()


def read_transactions_xlsx(file_path: str) -> Any:
    """
    Чтение финансовых операций из XLSX-файла.
    """
    logging.info(f"Чтение данных из файла {file_path}")
    try:
        opera_1 = pd.read_excel(file_path)  # Читаем файл Excel с помощью Pandas
        return opera_1.to_dict("records")  # Преобразуем DataFrame в список словарей
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден")
        return []


# Функция для простого поиска
def simple_search(transactions: Any, search_string: str) -> List[Dict]:
    """!!ARGS of functions:
    transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    """
    Простой поиск транзакций по описанию.

    Args:
        transactions: Список словарей с транзакциями.
        search_string: Строка поиска.

    Returns:
        Список словарей с транзакциями, соответствующими запросу.
    """
    logger.info(f"Поиск транзакций по строке '{search_string}'")
    return [
        transaction
        for transaction in transactions
        if "description" in transaction and re.search(search_string, transaction["description"])
    ]


def main_reports() -> None:
    """
    Главная функция модуля, объединяющая все функции в 1

    :return: None
    """
    operations = read_transactions_xlsx("../data/operations_mi.xls")
    print("Ведите что нужно найти")
    search_string = input()
    filtered_operations = simple_search(operations, search_string)

    with open("filtered_operations.json", "w", encoding="utf-8") as f:
        json.dump(filtered_operations, f, indent=4, ensure_ascii=False)  # indent для красивого формата

    logger.info("Отфильтрованные операции записаны в файл filtered_operations.json")
    print("Отфильтрованные операции записаны в файл filtered_operations.json")


if __name__ == "__main__":
    main_reports()
