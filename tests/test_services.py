import json
import os
from unittest.mock import patch
from typing import  Any
import pandas as pd
import pytest

from src.services import read_transactions_xlsx_file, simple_search


# Тест для функции read_transactions_xlsx_file
def test_read_transactions_xlsx_file() -> None:
    mock_data = {"Описание": ["Test description"], "Категория": ["Test category"], "Сумма": [100.0]}
    df = pd.DataFrame(mock_data)

    with patch("pandas.read_excel", return_value=df):
        result = read_transactions_xlsx_file("dummy_path")
        assert len(result) == 1
        assert result[0]["Описание"] == "Test description"
        assert result[0]["Категория"] == "Test category"
        assert result[0]["Сумма"] == 100.0

    with patch("pandas.read_excel", side_effect=Exception("File not found")):
        result = read_transactions_xlsx_file("dummy_path")
        assert result == []


# Тест для функции simple_search
def test_simple_search(tmpdir: Any) -> None:
    mock_data = [
        {"Описание": "Test description", "Категория": "Test category", "Сумма": 100.0},
        {"Описание": "Another description", "Категория": "Another category", "Сумма": 200.0},
    ]
    df = pd.DataFrame(mock_data)

    with patch("pandas.read_excel", return_value=df):
        output_file = os.path.join(tmpdir, "search_results.json")
        simple_search("Test", "dummy_path", output_file)

        with open(output_file, "r", encoding="utf-8") as f:
            result = json.load(f)

        assert len(result) == 1
        assert result[0]["Описание"] == "Test description"
        assert result[0]["Категория"] == "Test category"
        assert result[0]["Сумма"] == 100.0

        simple_search("Another", "dummy_path", output_file)

        with open(output_file, "r", encoding="utf-8") as f:
            result = json.load(f)

        assert len(result) == 1
        assert result[0]["Описание"] == "Another description"
        assert result[0]["Категория"] == "Another category"
        assert result[0]["Сумма"] == 200.0

        simple_search("Non-existing", "dummy_path", output_file)

        with open(output_file, "r", encoding="utf-8") as f:
            result = json.load(f)

        assert len(result) == 0


if __name__ == "__main__":
    pytest.main()
