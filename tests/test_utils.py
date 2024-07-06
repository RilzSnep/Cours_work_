from unittest.mock import MagicMock, patch
from typing import Any
import pandas as pd
import pytest

from src.utils import (
    format_top_transactions,
    get_currency_rate,
    get_greeting,
    get_stock_prices,
    load_api_key,
    process_cards,
    read_xls_file,
    summarize_cards,
)


@pytest.fixture(scope="module")
def mock_xls_data() -> Any:
    # Mock data for read_xls_file function
    return pd.DataFrame({"card_number": ["1234567890123456", "9876543210987654"], "transaction_amount": [100, -50]})


@pytest.fixture(scope="module")
def mock_cards_data() -> Any:
    # Mock data for process_cards function
    return [
        {"card_number": "1234567890123456", "transaction_amount": 100},
        {"card_number": "9876543210987654", "transaction_amount": -50},
    ]


@pytest.fixture(scope="module")
def mock_currency_data() -> Any:
    # Mock data for get_currency_rate function
    return {"Valute": {"USD": {"Value": 75.0}, "EUR": {"Value": 85.0}}}


@pytest.fixture(scope="module")
def mock_requests_get() -> Any:
    # Mock requests.get function
    mock_response = MagicMock()
    mock_response.json.return_value = {"Valute": {"USD": {"Value": 75.0}, "EUR": {"Value": 85.0}}}
    return mock_response


def test_read_xls_file(mock_xls_data: Any) -> None:
    # Test read_xls_file function
    file_path = "mock_data.xlsx"
    with patch("pandas.read_excel", return_value=mock_xls_data):
        result = read_xls_file(file_path)
        assert isinstance(result, list)
        assert len(result) == 2
        assert "transaction_amount" in result[0]


def test_process_cards(mock_cards_data: Any) -> None:
    # Test process_cards function
    cards, top_transactions = process_cards(mock_cards_data)
    assert isinstance(cards, dict)
    assert len(cards) == 2
    assert len(top_transactions) <= 5


def test_summarize_cards() -> None:
    # Test summarize_cards function
    cards = {
        "1234567890123456": {"total_amount": 100, "transactions": []},
        "9876543210987654": {"total_amount": 200, "transactions": []},
    }
    result = summarize_cards(cards)
    assert isinstance(result, list)
    assert len(result) == 2
    assert "last_digits" in result[0]
    assert "total_spent" in result[0]
    assert "cashback" in result[0]


def test_format_top_transactions() -> None:
    # Test format_top_transactions function
    top_transactions = [
        {"data_payment": "2023-07-10", "transaction_amount": 100, "category": "Food", "description": "Groceries"},
        {"data_payment": "2023-07-11", "transaction_amount": -50, "category": "Transport", "description": "Taxi"},
    ]
    result = format_top_transactions(top_transactions)
    assert isinstance(result, list)
    assert len(result) == 2
    assert "date" in result[0]
    assert "amount" in result[0]
    assert "category" in result[0]
    assert "description" in result[0]


def test_get_greeting() -> None:
    # Test get_greeting function
    result = get_greeting()
    assert isinstance(result, str)
    assert result in ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]


def test_get_currency_rate(mock_currency_data: Any, mock_requests_get: Any) -> None:
    # Test get_currency_rate function
    with patch("requests.get", return_value=mock_requests_get):
        result = get_currency_rate()
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["currency"] == "USD"
        assert result[1]["currency"] == "EUR"
        assert result[0]["rate"] == 75.0
        assert result[1]["rate"] == 85.0


def test_load_api_key(monkeypatch: Any) -> None:
    # Test load_api_key function
    mock_api_key = "mock_api_key"
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", mock_api_key)
    result = load_api_key()
    assert result == mock_api_key


def test_get_stock_prices(mock_requests_get: Any) -> None:
    # Test get_stock_prices function
    stock_symbols = ["AAPL", "AMZN"]
    with patch("requests.get", return_value=mock_requests_get):
        result = get_stock_prices(stock_symbols)
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["symbol"] == "AAPL"
        assert result[1]["symbol"] == "AMZN"


if __name__ == "__main__":
    pytest.main()
