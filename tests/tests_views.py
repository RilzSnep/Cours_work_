import unittest
from unittest.mock import Mock, patch

import pandas as pd

from src.views import (
    calculate_total_expenses,
    get_greeting,
    get_stock_currency,
    process_card_data,
    read_transactions_xlsx,
    top_transactions,
)


# Заглушки для внешних зависимостей
@patch('requests.get')
def mocked_requests_get(*args):
    """Заглушка для запросов к API.

    Возвращает моковый ответ с курсом RUB к USD, если timeout = 15,
    иначе возвращает пустой ответ.
    """
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0].timeout == 15:
        return MockResponse({"rates": {"RUB": 70}}, 200)
    else:
        return MockResponse({}, 404)


class TestFunctions(unittest.TestCase):
    """Тестовый класс для функций из модуля src.views."""

    def setUp(self):
        """Настройка перед каждым тестом."""
        pass

    def test_get_greeting(self):
        """Проверяет работу функции get_greeting для разных времен."""
        self.assertEqual(get_greeting("2022-04-01 12:00:00"), "Добрый день")
        self.assertEqual(get_greeting("2022-04-01 06:00:00"), "Доброе утро")
        self.assertEqual(get_greeting("2022-04-01 18:00:00"), "Добрый вечер")
        self.assertEqual(get_greeting("2022-04-01 00:00:00"), "Доброй ночи")

    @patch('yfinance.Ticker')
    def test_get_stock_currency(self, mock_ticker):
        """Проверяет работу функции get_stock_currency."""
        mock_data = Mock()
        mock_data.history.return_value = pd.DataFrame({'High': [100]})
        mock_ticker.return_value = mock_data
        self.assertEqual(get_stock_currency("AAPL"), 100)

    def test_calculate_total_expenses(self):
        """Проверяет работу функции calculate_total_expenses."""
        transactions = [{'transaction_amount': -100}, {'transaction_amount': -200}]
        self.assertEqual(calculate_total_expenses(transactions), -300)

    def test_read_transactions_xlsx(self):
        """Проверяет работу функции read_transactions_xlsx."""
        with patch('pandas.read_excel', return_value=pd.DataFrame({})):
            self.assertIsNone(read_transactions_xlsx("non_existent_file.xls"))

    def test_empty_operations(self):
        """Проверяет работу функции process_card_data с пустым списком операций."""
        operations = []
        self.assertEqual(process_card_data(operations), [])

    def test_single_card_transaction(self):
        """Проверяет работу функции process_card_data с одной транзакцией по одной карте."""
        operations = [
            {
                "card_number": "*1234567890123456",
                "transaction_amount": -100.0,
                "bonuses_including_cashback": 5.0
            }
        ]
        expected_result = [
            {
                "last_digits": "3456",
                "total_spent": 100.0,
                "cashback": 5.0
            }
        ]
        self.assertEqual(process_card_data(operations), expected_result)

    def test_top_transactions(self):
        """Проверяет работу функции top_transactions."""
        transactions = [{'transaction_amount': -100}, {'transaction_amount': -200}]
        self.assertEqual(top_transactions(transactions),
                         [{'date': '', 'amount': -200, 'category': '', 'description': ''}])


if __name__ == '__main__':
    unittest.main()
