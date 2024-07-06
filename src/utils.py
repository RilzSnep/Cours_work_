import logging
import os  # Добавлен импорт модуля os
from datetime import datetime
from typing import Any
import pandas as pd
import requests

# Настройка логгера для модуля utils
logger = logging.getLogger(__name__)


def read_xls_file(file_path: Any) -> list:
    """
    Read the XLS file and return the data as a list of dictionaries.

    Args:
        file_path (Any): Path to the XLS file.

    Returns:
        list: List of dictionaries representing the data from the XLS file.
    """
    try:
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error("Ошибка при чтении файла %s: %s", file_path, str(e))
        return []


def process_cards(data: Any) -> tuple:
    """
    Process the card data to return a summary.

    Args:
        data (Any): Input data to process.

    Returns:
        tuple: A tuple containing a dictionary of cards and a list of top transactions.
    """
    cards = {}
    for row in data:
        card_number = str(row.get("card_number", "unknown"))
        amount = row.get("transaction_amount", 0)

        if pd.isna(card_number):
            card_number = "unknown"

        if card_number not in cards:
            cards[card_number] = {"total_amount": 0, "transactions": []}

        cards[card_number]["total_amount"] += amount
        cards[card_number]["transactions"].append(row)

    top_transactions = sorted(data, key=lambda x: abs(x.get("transaction_amount", 0)), reverse=True)[:5]

    return cards, top_transactions


def summarize_cards(cards: Any) -> list:
    """
    Create a summary of the card data.

    Args:
        cards (Any): Input card data to summarize.

    Returns:
        list: List of dictionaries containing summarized card information.
    """
    summary = []
    for card_number, info in cards.items():
        summary.append(
            {
                "last_digits": card_number[-4:] if card_number != "unknown" else "unknown",
                "total_spent": round(info["total_amount"], 2),
                "cashback": round(info["total_amount"] * 0.01, 2),  # Assuming cashback is 1% of total spent
            }
        )
    return summary


def format_top_transactions(top_transactions: Any) -> list:
    """
    Format the top transactions.

    Args:
        top_transactions (Any): Input top transactions to format.

    Returns:
        list: List of dictionaries containing formatted transaction information.
    """
    formatted_transactions = []
    for transaction in top_transactions:
        formatted_transactions.append(
            {
                "date": transaction.get("data_payment", "unknown"),
                "amount": transaction.get("transaction_amount", 0),
                "category": transaction.get("category", "unknown"),
                "description": transaction.get("description", "unknown"),
            }
        )
    return formatted_transactions


def get_greeting() -> str:
    """
    Return a greeting based on the current time.

    Returns:
        str: Greeting message based on the current time of the day.
    """
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_currency_rate() -> list:
    """
    Get USD and EUR exchange rates from the Central Bank of Russia.

    Returns:
        list: List of dictionaries containing currency rates.
    """
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        data = response.json()
        usd_rate = data["Valute"]["USD"]["Value"]
        eur_rate = data["Valute"]["EUR"]["Value"]
        return [{"currency": "USD", "rate": usd_rate}, {"currency": "EUR", "rate": eur_rate}]
    except Exception as e:
        logger.error("Ошибка при получении курсов валют: %s", str(e))
        return []


def load_api_key() -> Any:
    """
    Load API key from .env file.

    Returns:
        Any: API key string if found, otherwise None.
    """
    try:
        from dotenv import load_dotenv

        load_dotenv()
        return os.getenv("ALPHAVANTAGE_API_KEY")
    except Exception as e:
        logger.error("Ошибка при загрузке API ключа: %s", str(e))
        return None


def get_stock_prices(symbols: Any) -> list:
    """
    Get stock prices for given symbols using Alpha Vantage API.

    Args:
        symbols (Any): List of stock symbols.

    Returns:
        list: List of dictionaries containing stock symbols and their prices.
    """
    try:
        api_key = load_api_key()
        if not api_key:
            raise ValueError("API key not found. Make sure to set ALPHAVANTAGE_API_KEY in your .env file.")

        prices = []
        base_url = "https://www.alphavantage.co/query"
        for symbol in symbols:
            params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": api_key}
            response = requests.get(base_url, params=params)
            data = response.json()

            if "Global Quote" in data:
                price = float(data["Global Quote"]["05. price"])
                prices.append({"symbol": symbol, "price": price})
            else:
                prices.append({"symbol": symbol, "price": "Not available"})

        return prices

    except Exception as e:
        logger.error("Ошибка при получении цен на акции: %s", str(e))
        return []


def get_card_summary(file_path: Any, analysis_date: Any=None) -> dict:
    """
    Get the card summary from the XLS file.

    Args:
        file_path (Any): Path to the XLS file.
        analysis_date (Any, optional): Analysis date. Defaults to None.

    Returns:
        dict: Dictionary containing the card summary information.
    """
    data = read_xls_file(file_path)
    cards, top_transactions = process_cards(data)
    summary = summarize_cards(cards)
    formatted_top_transactions = format_top_transactions(top_transactions)
    currency_rates = get_currency_rate()

    result = {
        "greeting": get_greeting(),
        "cards": summary,
        "top_transactions": formatted_top_transactions,
        "currency_rates": currency_rates,
    }

    return result
