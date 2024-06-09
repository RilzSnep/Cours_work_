import json

import pandas as pd


def get_transactions_by_keyword(search_term_2: str) -> str:
    """Возвращает JSON-ответ со всеми транзакциями, содержащими search_term
    в описании или категории.

    Args:
        search_term_2: Строка для поиска.

    Returns:
        JSON-строка с результатами поиска.
    """
    try:
        file_path = "../data/operations_mi.xls"
        data = pd.read_excel(file_path)

        # Фильтруем данные
        filtered_data = data[
            data["description"].str.contains(search_term_2, case=False)
            | data["category"].str.contains(search_term_2, case=False)
        ]

        # Преобразуем DataFrame в список словарей
        transaction_list = filtered_data.to_dict(orient="records")

        # Проверяем, пустой ли список
        if not transaction_list:
            transaction_list = [{"message": "Слово не найдено ни в одной категории"}]

        # Преобразуем список словарей в JSON-строку
        json_response = json.dumps(transaction_list, indent=4, ensure_ascii=False)

        # Записываем в файл
        with open("transactions_search_result.json", "w", encoding="utf-8") as f:
            json.dump(transaction_list, f, indent=4, ensure_ascii=False)

        return json_response

    except FileNotFoundError:
        return json.dumps({"error": "Файл operations.xls не найден."}, indent=4, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Произошла ошибка: {str(e)}"}, indent=4, ensure_ascii=False)


# Пример использования:
search_term_1 = "кафе"
json_result = get_transactions_by_keyword(search_term_1)
print(json_result)
