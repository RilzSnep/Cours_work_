import json
from datetime import datetime, timedelta
from typing import Any

import pandas as pd

# Предположим, что функция ligging_setup уже определена в модуле src.utils
from src.utils import ligging_setup

logger = ligging_setup()


def read_transactions_xlsx(file_path: str) -> pd.DataFrame:
    """
    Чтение финансовых операций из XLSX-файла.
    """
    logger.info(f"Чтение данных из файла {file_path}")
    try:
        return pd.read_excel(file_path)  # Читаем файл Excel с помощью Pandas
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден")
        return pd.DataFrame()  # Возвращаем пустой DataFrame в случае ошибки


def filter_transactions_by_category_and_date(
    transactions: pd.DataFrame, category: str, start_date: str
) -> list[dict[Any, Any]]:
    """
    Фильтрация транзакций по категории и дате.

    Args:
        transactions: DataFrame с транзакциями.
        category: Категория для фильтрации.
        start_date: Дата начала 3-месячного периода в формате 'YYYY-MM-DD'.

    Returns:
        Список словарей с транзакциями, соответствующими запросу.
    """
    end_date = datetime.strptime(start_date, "%d.%m.%Y") + timedelta(days=90)
    filtered_transactions = transactions[
        (transactions['category'] == category) &
        (transactions['data_payment'] >= start_date) &
        (transactions['data_payment'] < end_date.strftime("d.%m.%Y"))
    ]
    return filtered_transactions.to_dict('records')


def main_reports() -> None:
    """
    Главная функция модуля.
    """
    operations = read_transactions_xlsx("../data/operations_mi.xls")
    category = input("Введите категорию трат: ")
    start_date = input("Введите дату начала 3-месячного периода (MM.DD.YYYY): ")

    filtered_operations = filter_transactions_by_category_and_date(operations, category, start_date)

    with open("filtered_operations.json", "w", encoding="utf-8") as f:
        json.dump(filtered_operations, f, indent=4, ensure_ascii=False)

    logger.info("Отфильтрованные операции записаны в файл filtered_operations.json")
    print("Отфильтрованные операции записаны в файл filtered_operations.json")


if __name__ == "__main__":
    main_reports()
