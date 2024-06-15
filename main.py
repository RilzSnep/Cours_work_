from src.views import main_views
from src.reports import main_reports
from src.services import main_servies


def main() -> None:
    """ вызов всех функций """
    main_views()
    main_reports()
    main_servies()


if __name__ == "__main__":
    main()
