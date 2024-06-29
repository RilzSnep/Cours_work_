import json
import logging
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
def simple_search(transactions: List[Dict], search_data: List[Dict]) -> List[Dict]:
    """
    Простой поиск транзакций по данным из JSON.

    Args:
        transactions: Список словарей с транзакциями.
        search_data: Список словарей с данными для поиска.

    Returns:
        Список словарей с транзакциями, соответствующими запросу.
    """
    logger.info(f"Поиск транзакций по данным: {search_data}")

    filtered_transactions = []
    for search_item in search_data:
        for transaction in transactions:
            if all(item in transaction.items() for item in search_item.items()):
                filtered_transactions.append(transaction)
    return filtered_transactions


def main_reports() -> None:
    """
    Главная функция модуля.
    """
    operations = read_transactions_xlsx("../data/operations_mi.xls")
    print("Введите данные для поиска в формате JSON:")
    # [{"name": "Алексей"}]
    search_string = input()

    try:
        search_data = json.loads(search_string)
    except json.JSONDecodeError:
        logger.error("Некорректный формат JSON.")
        print("Ошибка: некорректный формат JSON.")
        return

    filtered_operations = simple_search(operations, search_data)

    with open("filtered_operations.json", "w", encoding="utf-8") as f:
        json.dump(filtered_operations, f, indent=4, ensure_ascii=False)

    logger.info("Отфильтрованные операции записаны в файл filtered_operations.json")
    print("Отфильтрованные операции записаны в файл filtered_operations.json")


if __name__ == "__main__":
    main_reports()
