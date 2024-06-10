import json
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import requests
import yfinance as yf

API_KEY = os.getenv("api_key")


def get_greeting(date_time_str_1: str) -> str:
    """
    функция принимает строку с датой и временем и возвращает приветствие в зависимости от времени суток
    """
    date_time = datetime.strptime(date_time_str_1, "%Y-%m-%d %H:%M:%S")
    hour = date_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def calculate_total_expenses(transactions: List[Dict[str, Any]]) -> int:
    """
    Функция вычисляет общую сумму расходов по списку транзакций
    """
    total_expenses = 0
    for transaction in transactions:
        if transaction["transaction_amount"] < 0:
            total_expenses += transaction["transaction_amount"]
    return total_expenses


def read_transactions_xlsx(file_path: str) -> Any:
    """
    Эта функция читает данные о транзакциях из файла Excel
    """
    opera_1 = pd.read_excel(file_path)
    return opera_1.to_dict("records")


reader = read_transactions_xlsx("../data/operations_mi.xls")


def process_card_data(operations_1: List[Dict[str, Any]]) -> Any:
    """
    Эта функция обрабатывает данные о картах из списка транзакций
    """
    card_data = {}
    for operation in operations_1:
        if isinstance(operation["card_number"], str) and operation["card_number"].startswith("*"):
            last_digits = operation["card_number"][-4:]
            if last_digits not in card_data:
                card_data[last_digits] = {"last_digits": last_digits, "total_spent": 0, "cashback": 0}
            if operation["transaction_amount"] < 0:
                card_data[last_digits]["total_spent"] -= round(operation["transaction_amount"], 1)
            card_data[last_digits]["cashback"] += operation.get("bonuses_including_cashback", 0)
    return list(card_data.values())


def top_transactions(reader: List[Dict[str, Any]]) -> Any:
    """
    Функция возвращает список из пяти самых дорогих транзакций
    """
    if reader is not None:

        def sort_by_sum(item: Any) -> Any:
            return item["transaction_amount"]

        reader.sort(key=sort_by_sum, reverse=True)
        result = []
        i = 0
        for transaction in reader:
            if i < 5:
                result.append(
                    {
                        "date": transaction["date_operation"],
                        "amount": transaction["transaction_amount"],
                        "category": transaction["category"],
                        "description": transaction["description"],
                    }
                )
                i += 1
            else:
                break
        return result
    else:
        return None


rate_1 = []  # Define an empty list before appending values to it
rate_2 = []


def get_currency_rate(currency: str) -> Any:
    """
    Эта функция получает курс валюты по отношению к рублю с использованием API
    """
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    headers = {"apikey": "zreg2uCOFNUBn4Or2wvNJ1VlpSF22ByN"}
    response = requests.get(url, headers=headers, timeout=15)
    response_data = json.loads(response.text)
    rate = response_data["rates"]["RUB"]
    return rate


def get_stock_currency(stock: str) -> Any:
    """
    Функция получает текущую цену акции с помощью Yahoo Finance
    """
    data = yf.Ticker(stock)
    todays = pd.DataFrame(data.history(period="1d"))
    todays_dict = todays.to_dict(orient="records")
    return todays_dict[0]["High"]


rate_1.append({"currency": "USD", "rate": round(get_currency_rate("USD"), 2)})
rate_1.append({"currency": "EUR", "rate": round(get_currency_rate("EUR"), 2)})
rate_2.append(
    [
        {"stock": "AAPL", "price": round(get_stock_currency("AAPL"), 2)},
        {"stock": "AMZN", "price": round(get_stock_currency("AMZN"), 2)},
        {"stock": "GOOGL", "price": round(get_stock_currency("GOOGL"), 2)},
        {"stock": "MSFT", "price": round(get_stock_currency("MSFT"), 2)},
        {"stock": "TSLA", "price": round(get_stock_currency("TSLA"), 2)},
    ]
)


operations = read_transactions_xlsx("../data/operations_mi.xls")
total_expenses = calculate_total_expenses(operations)
card_data = process_card_data(operations)
top_transactions = top_transactions(reader)

output_data = {
    "greeting": get_greeting(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    "cards": card_data,
    "top_transactions": top_transactions,
    "currency_rates": rate_1,
    "stock_prices": rate_2,
}

output_file = "operations_data.json"
"""
лткрытие файла для записей и сразу записывает
"""
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=4, ensure_ascii=False)
