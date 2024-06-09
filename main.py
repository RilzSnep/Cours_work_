import json
import os


def read_and_print_data(file_path: str) -> None:
    """Читает JSON-файл и выводит курс валют и цены акций."""
    try:
        if not os.path.isfile(file_path):
            print(f"Файл {file_path} не найден.")
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        # Извлечение данных о курсах валют
        currency_rates = data.get("currency_rates", [])
        print("Курсы валют:")
        for rate in currency_rates:
            print(f"{rate['currency']}: {rate['rate']}")

        # Извлечение данных о ценах акций
        stock_prices = data.get("stock_prices", [])
        print("\nСтоимость акций из S&P 500:")
        for stock in stock_prices:
            print(f"{stock['stock']}: {stock['price']}")

    except json.JSONDecodeError:
        print(f"Ошибка при декодировании JSON в файле {file_path}.")


# Пример использования
# 1. Если папка "data" находится на одном уровне с вашим скриптом:
file_path = os.path.join(os.path.dirname(__file__), "data", "operations.json")
read_and_print_data(file_path)

# 2. Если папка "data" находится на более высоком уровне:
# file_path = os.path.join(os.path.dirname(__file__), "..", "data", "operations.json")
# read_and_print_data(file_path)

# 3. Если вы знаете полный путь к файлу:
# file_path = "C:/Users/YourUsername/Documents/data/operations.json"
# read_and_print_data(file_path)
