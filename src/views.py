import json
import os
from datetime import datetime
from typing import Any, Dict, List

import requests
import yfinance as yf
from dotenv import load_dotenv

from src.utils import read_transactions_json, read_transactions_xlsx, write_transactions_json

load_dotenv()
# Получение API ключа из переменных окружения
API_KEY = os.getenv("api_key")


def get_greeting(date_time_str: str | None) -> str:
    """
    Функция принимает строку с датой и временем (необязательно)
    и возвращает приветствие в зависимости от времени суток.
    """
    if date_time_str is None:
        date_time = datetime.now()
    else:
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    hour = date_time.hour
    if 5 <= hour < 12:
        return "Доброе утро!"
    elif 12 <= hour < 18:
        return "Добрый день!"
    elif 18 <= hour < 23:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


def calculate_total_expenses(transactions: List[Dict[str, Any]]) -> float:
    """
    Функция вычисляет общую сумму расходов по списку транзакций.
    """
    total_expenses = 0.0
    for transaction in transactions:
        if transaction["transaction_amount"] < 0:
            total_expenses += transaction["transaction_amount"]
    return total_expenses * -1


def process_card_data(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Эта функция обрабатывает данные о картах из списка транзакций.
    """
    card_data = {}
    for operation in operations:
        if isinstance(operation["card_number"], str) and operation["card_number"].startswith("*"):
            last_digits = operation["card_number"][-4:]
            if last_digits not in card_data:
                card_data[last_digits] = {"last_digits": last_digits, "total_spent": 0.0, "cashback": 0.0}
            if operation["transaction_amount"] < 0:
                card_data[last_digits]["total_spent"] += round(operation["transaction_amount"] * -1, 1)
            card_data[last_digits]["cashback"] += operation.get("bonuses_including_cashback", 0.0)
    return list(card_data.values())


def top_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Функция возвращает список из пяти самых дорогих транзакций.
    """
    transactions.sort(key=lambda x: x["transaction_amount"], reverse=True)
    return transactions[:5]


def get_currency_rate(currency: str) -> Any:
    """
    Эта функция получает курс валюты по отношению к рублю с использованием API.
    """
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    response = requests.get(url, headers={"apikey": API_KEY}, timeout=40)
    response_data = json.loads(response.text)
    return response_data["rates"]["RUB"]


def get_stock_currency(stock: str) -> Any:
    """
    Функция получает текущую цену акции с помощью Yahoo Finance.
    """
    stock_data = yf.Ticker(stock)
    todays_data = stock_data.history(period="1d")
    return todays_data["High"].iloc[0]


def main_views() -> None:
    """
    Главная функция программы, запускающая обработку транзакций.
    """
    # Запрос у пользователя даты и времени
    user_input = input(
        "Введите дату и время в формате YYYY-MM-DD HH:MM:SS " "или нажмите Enter для использования текущего времени: "
    )
    greeting = get_greeting(user_input if user_input else None)
    # print(greeting)

    transactions = read_transactions_xlsx("../data/operations_mi.xls")
    total_expenses = calculate_total_expenses(transactions)
    # print(f"Total expenses: {total_expenses}")

    card_data = process_card_data(transactions)
    # print(f"Card data: {card_data}")

    top_trans = top_transactions(transactions)
    # print(f"Top transactions: {top_trans}")

    currency_rates = [
        {"currency": "USD", "rate": get_currency_rate("USD")},
        {"currency": "EUR", "rate": get_currency_rate("EUR")},
    ]
    # print(f"Currency rates: {currency_rates}")

    stock_prices = [
        {"stock": "AAPL", "price": get_stock_currency("AAPL")},
        {"stock": "AMZN", "price": get_stock_currency("AMZN")},
        {"stock": "GOOGL", "price": get_stock_currency("GOOGL")},
        {"stock": "MSFT", "price": get_stock_currency("MSFT")},
        {"stock": "TSLA", "price": get_stock_currency("TSLA")},
    ]
    # print(f"Stock prices: {stock_prices}")

    output_data = {
        "greeting": greeting,
        "total_expenses": total_expenses,
        "card_data": card_data,
        "top_transactions": top_trans,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    output_file = "operations_data.json"
    write_transactions_json(output_file, output_data)
    print(read_transactions_json(output_file))


if __name__ == "__main__":
    main_views()
