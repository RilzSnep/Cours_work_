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


if __name__ == "__main__":
    unittest.main()
