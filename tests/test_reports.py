import unittest
from typing import Any

import pandas as pd
from pytest import fixture

from src.reports import read_transactions_xlsx, simple_search


@fixture
def operations(tmp_path: Any) -> Any:
    # Создаем временный файл XLSX с данными для теста
    data = {"date": ["2022-01-01", "2022-01-02"], "description": ["Salary", "Rent"], "amount": [1000, -500]}
    df = pd.DataFrame(data)
    file_path = tmp_path / "transactions.xlsx"
    df.to_excel(file_path, index=False)
    return file_path


class TestMyFunctions(unittest.TestCase):
    def setUp(self) -> None:
        # Set up any data needed for the tests
        self.operations = [
            {"description": "Transaction 1"},
            {"description": "Transaction 2"},
            {"description": "Transaction with Магнит"},
            {"description": "Another transaction with Магнит"},
            {"description": "Transaction without search string"},
        ]
        self.search_string = "Магнит"

    def test_search_transactions(self) -> None:
        # Test if read_transactions_xlsx returns a list of dictionaries
        file_path = "test_file.xlsx"  # Provide a test file path
        transactions = simple_search(file_path, "")
        self.assertIsInstance(transactions, list)
        for transaction in transactions:
            self.assertIsInstance(transaction, dict)

    def test_search_other_transactions(self) -> None:
        # Test if search_transactions filters transactions correctly
        filtered_operations = simple_search(self.operations, self.search_string)
        self.assertEqual(len(filtered_operations), 2)  # Expecting 2 transactions containing "Магнит"

        # Check if filtered operations contain transactions with the search string
        for transaction in filtered_operations:
            self.assertIn(self.search_string, transaction["description"])


def test_read_transactions_xlsx(operations: Any) -> None:
    # Вызываем функцию и проверяем результат
    transactions = read_transactions_xlsx(operations)
    assert len(transactions) == 2
    assert transactions[0] == {"date": "2022-01-01", "description": "Salary", "amount": 1000}
    assert transactions[1] == {"date": "2022-01-02", "description": "Rent", "amount": -500}


class TestSimpleSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.transactions = [
            {"description": "Purchase of a book", "amount": 25.0},
            {"description": "Grocery shopping", "amount": 100.0},
            {"description": "Movie ticket purchase", "amount": 15.0},
        ]

    def test_simple_search_with_matching_string(self) -> None:
        search_string = "book"
        expected_result = [
            {"description": "Purchase of a book", "amount": 25.0},
        ]
        result = simple_search(self.transactions, search_string)
        self.assertEqual(result, expected_result)

    def test_simple_search_with_non_matching_string(self) -> None:
        search_string = "car"
        expected_result: list = []
        result = simple_search(self.transactions, search_string)
        self.assertEqual(result, expected_result)


class TestReadTransactionsXlsx(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_data: list = []

    def test_read_transactions_xlsx_with_valid_file(self) -> None:
        df = pd.DataFrame(self.mock_data)
        df.to_dict = lambda x: self.mock_data

        file_path = "mock_file.xlsx"

        def mock_read_excel(file_path: Any) -> Any:
            return df

        read_transactions_xlsx.__globals__["pd.read_excel"] = mock_read_excel

        result = read_transactions_xlsx(file_path)
        self.assertEqual(result, self.mock_data)

    def test_read_transactions_xlsx_with_invalid_file(self) -> None:
        file_path = "invalid_file.xlsx"

        def mock_read_excel(file_path: Any) -> Any:
            raise FileNotFoundError

        read_transactions_xlsx.__globals__["pd.read_excel"] = mock_read_excel

        result = read_transactions_xlsx(file_path)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
