import logging
from logging import Logger
from typing import Any

import pandas as pd


def ligging_setup() -> Logger:
    """
    Настройка логирования.
    """
    # Настройка корневого логгера
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        filename="search_log.txt",
        filemode="w",
    )
    # Создание и возвращение объекта Logger
    logger = logging.getLogger(__name__)
    return logger


def read_transactions_xlsx(file_path: str) -> Any:
    """
    Эта функция читает данные о транзакциях из файла Excel.
    """
    transactions_df = pd.read_excel(file_path)
    return transactions_df.to_dict("records")
