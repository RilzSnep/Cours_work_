import json
import logging
import os
from typing import Any
from datetime import datetime

from dotenv import load_dotenv

from src.utils import get_card_summary, get_stock_prices

# Настройка логгера
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_api_key() -> Any:
    """
    Load API key from .env file.
    """
    load_dotenv()
    return os.getenv("ALPHAVANTAGE_API_KEY")


if __name__ == "__main__":
    """
    Main execution block.

    Prompts the user for a date or uses the current date if none is provided.
    Then, it processes financial operations from a file and fetches current stock prices.
    Finally, it prints the results in JSON format.
    """
    # Запрашиваем у пользователя дату или используем текущую дату
    user_date_input = input("Введите дату в формате DD.MM.YYYY (Нажмите Enter чтобы использовать текущую дату): ")
    if user_date_input.strip():
        try:
            analysis_date = datetime.strptime(user_date_input, "%d.%m.%Y")
        except ValueError:
            logger.error("Неверный формат даты. Используется текущая дата.")
            analysis_date = datetime.now()
    else:
        analysis_date = datetime.now()

    file_path = "../data/operations.xls"

    try:
        result = get_card_summary(file_path, analysis_date)

        stock_symbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        stock_prices = get_stock_prices(stock_symbols)

        result["stock_prices"] = stock_prices

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        logger.exception("Ошибка при выполнении программы: %s", str(e))
