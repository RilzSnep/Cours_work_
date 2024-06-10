import json
import re
from typing import Any, Dict, List

import pandas as pd


def read_transactions_xlsx(file_path: str) -> List[Dict]:
    """
    Чтение финансовых операций из XLSX-файла.
    """
    opera_1 = pd.read_excel(file_path)  # Читаем файл Excel с помощью Pandas
    return opera_1.to_dict("records")  # Преобразуем DataFrame в список словарей


operations = read_transactions_xlsx("../data/operations_mi.xls")
search_string = "Магнит"


def search_transactions(operations_1: Any, search_string_1: Any) -> list[dict[str, Any]]:
    """
    Фильтрация списка словарей, проверяя наличие строки поиска в описании.

    Args:
        operations_1: Список словарей с транзакциями.
        search_string_1: Строка поиска.

    Returns:
        Отфильтрованный список словарей с транзакциями.
    """
    return [
        transaction
        for transaction in operations_1
        if "description" in transaction and re.search(search_string_1, transaction["description"])
    ]


filtered_operations = search_transactions(operations, search_string)

# Запись в JSON-файл
with open("filtered_operations.json", "w", encoding="utf-8") as f:
    json.dump(filtered_operations, f, indent=4, ensure_ascii=False)  # indent для красивого формата

print("Отфильтрованные операции записаны в файл filtered_operations.json")
