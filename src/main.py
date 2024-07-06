import json
import logging
from datetime import datetime
from reports import main_reports
from services import simple_search
from utils import get_card_summary, get_stock_prices

# Настройка логгера
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Основная функция программы.

    Пример использования функций из различных модулей:
    - Используется функция simple_search для выполнения поиска транзакций в файле XLSX.
    - Используется функция get_card_summary для получения сводной информации о картах из файла XLS.
    - Используется функция get_stock_prices для получения текущих цен на акции.
    - Используется функция main_reports для выполнения отчетов
    """
    try:
        # Пример использования функций из utils.py
        file_path = "../data/operations.xls"
        user_request = input("Введите запрос для поиска: ")
        output_file = "search_results.json"
        simple_search(user_request, file_path, output_file)
        print(f"Результаты поиска сохранены в файл: {output_file}")

        # Пример использования функций из views.py
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
        result = get_card_summary(file_path, analysis_date)

        stock_symbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        stock_prices = get_stock_prices(stock_symbols)

        result["stock_prices"] = stock_prices

        print(json.dumps(result, ensure_ascii=False, indent=2))

        # Пример использования функций из reports.py
        main_reports()

    except Exception as e:
        logger.exception("Ошибка при выполнении программы: %s", str(e))


if __name__ == "__main__":
    main()
