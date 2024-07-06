import json
import logging
from typing import Any
import pandas as pd

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_transactions_xlsx_file(file_path: str) -> list:
    """
    Чтение транзакций из файла XLSX и возврат данных в формате списка словарей.
    """
    try:
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
    except pd.errors.EmptyDataError:
        logger.error(f"Файл {file_path} пустой или не содержит данных")
        return []
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        return []


def simple_search(user_request: str, file_path: str, output_file: str) -> None:
    """
    Функция выполняет простой поиск по данным транзакций и записывает результат в файл JSON.
    """
    logger.info("start simple_search")
    python_data = read_transactions_xlsx_file(file_path)
    data = []
    for transaction in python_data:
        # Поиск по описанию и категории (учитывая регистр)
        if (user_request.lower() in str(transaction.get("Описание", "")).lower()) or (
            user_request.lower() in str(transaction.get("Категория", "")).lower()
        ):
            data.append(transaction)

        # Обработка пустых значений (NaN) в данных
        for key, value in transaction.items():
            if pd.isna(value):
                transaction[key] = None

    # Запись результатов поиска в файл JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f"Результаты поиска сохранены в файл: {output_file}")


if __name__ == "__main__":
    file_path = "../data/operations.xls"  # Путь к вашему файлу с данными
    user_request = input("Введите запрос для поиска: ")
    output_file = "search_results.json"  # Путь к файлу, куда будут сохранены результаты поиска
    simple_search(user_request, file_path, output_file)
    print(f"Результаты поиска сохранены в файл: {output_file}")
