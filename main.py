from src.reports import spending_by_category
from src.services import analyze_cashback
from src.utils import read_xlsx
from src.views import main_info

if __name__ == "__main__":
    # print(main_info("2018-05-03 15:30:00"))
    # print(analyze_cashback("data/operations.xlsx", 2021, 5))
    transactions_df = read_xlsx("data/operations.xlsx")
    print(spending_by_category(transactions_df, "Супермаркеты", "2018-05-03 15:30:00"))
