import unittest

from src.reports import search_transactions


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
        transactions = search_transactions(file_path, "")
        self.assertIsInstance(transactions, list)
        for transaction in transactions:
            self.assertIsInstance(transaction, dict)

    def test_search_other_transactions(self) -> None:
        # Test if search_transactions filters transactions correctly
        filtered_operations = search_transactions(self.operations, self.search_string)
        self.assertEqual(len(filtered_operations), 2)  # Expecting 2 transactions containing "Магнит"

        # Check if filtered operations contain transactions with the search string
        for transaction in filtered_operations:
            self.assertIn(self.search_string, transaction["description"])


if __name__ == "__main__":
    unittest.main()
