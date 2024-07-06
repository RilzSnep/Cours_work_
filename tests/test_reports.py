from unittest.mock import patch
from typing import Any
import pytest

from src.views import load_api_key


@pytest.fixture(scope="module")
def mock_load_dotenv() -> Any:
    # Мок load_dotenv из dotenv
    with patch("dotenv.load_dotenv"):
        yield


@pytest.fixture(scope="module")
def mock_get_stock_prices() -> Any:
    # Мок get_stock_prices из utils
    with patch("views.get_stock_prices") as mock:
        mock.return_value = [{"symbol": "AAPL", "price": 150.0}, {"symbol": "AMZN", "price": 3000.0}]
        yield mock


def test_load_api_key(mock_load_dotenv: Any) -> None:
    # Тест load_api_key из views
    mock_api_key = "mock_api_key"
    with patch("os.getenv", return_value=mock_api_key):
        result = load_api_key()
        assert result == mock_api_key


if __name__ == "__main__":
    pytest.main()