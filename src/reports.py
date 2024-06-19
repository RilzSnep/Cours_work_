import json
import logging
import re
from typing import Any, Dict, List

import pandas as pd

logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    filename="search_log.txt",  # Файл для записи логов
    filemode="w",  # Режим записи в файл (w - перезапись, a - добавление)
)


def read_transactions_xlsx(file_path: str) -> List[Dict]:
    """
    Чтение финансовых операций из XLSX-файла.
    """
    logging.info(f"Чтение данных из файла {file_path}")
    try:
        opera_1 = pd.read_excel(file_path)  # Читаем файл Excel с помощью Pandas
        return opera_1.to_dict("records")  # Преобразуем DataFrame в список словарей
    except FileNotFoundError:
        logging.error(f"Файл {file_path} не найден")
        return []


# Функция для простого поиска
def simple_search(transactions: Any, search_string: str) -> List[Dict]:
    """
    Простой поиск транзакций по описанию.

    Args:
        transactions: Список словарей с транзакциями.
        search_string: Строка поиска.

    Returns:
        Список словарей с транзакциями, соответствующими запросу.
    """
    logging.info(f"Поиск транзакций по строке '{search_string}'")
    return [
        transaction
        for transaction in transactions
        if "description" in transaction and re.search(search_string, transaction["description"])
    ]


def main_reports() -> None:
    operations = read_transactions_xlsx("../data/operations_mi.xls")
    search_string = input()
    filtered_operations = simple_search(operations, search_string)

    with open("filtered_operations.json", "w", encoding="utf-8") as f:
        json.dump(filtered_operations, f, indent=4, ensure_ascii=False)  # indent для красивого формата

    logging.info("Отфильтрованные операции записаны в файл filtered_operations.json")
    print("Отфильтрованные операции записаны в файл filtered_operations.json")


if __name__ == "__main__":
    main_reports()
