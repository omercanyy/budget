from libs.bank_statement import BankStatementInput
from libs.budget_v2 import BudgetV2


if __name__ == '__main__':
    # Category keywords
    # Either enter
    #   i) a category name to list of strings
    # or
    #  ii) a group by name to dictionary of (i)
    # group by names will be used to preview high level breakdowns
    break_down_details = {
        "Savings": {
            "Cash Savings": ["Online Transfer to SAV|000"],
        },
        "Accommodation": {
            "Rent": ["Cambridge Park 2069795813"],
            "Utils": ["comcast", "seattle city lights"],
            "Energy": ["SEATTLE CITY LIGHT"],
        },
        "Transportation": {
            "Car": ["Online Transfer to SAV|313"],
            "Car Insurance": ["PROG DIRECT INS  INS PREM", "PROG DIRECT INS"],
            "Gas": ["CHEVRON"]
        },
        "Bills": {
            "Internet": ["COMCAST CABLE COMM"],
            "Streaming": ["Prime Video", "peacock", "disney", "hulu", "spotify"],
            "Phone": ["Zelle payment to Omer Faruk Aslan|29"],
            "Other": ["labcor", "public storage", "safe deposit box", "educative"],
        },
        "Food + Groceries": {
            "Eating Out + Catering": ["DOORDASH", "DUTCH BROS", "Starbucks", "fresh flours",
                                      "common ground coffee", "kubra", "PARADISE RESTAURAN SEATTLE"],
            "Groceries": ["FRED MEYER", "DK MARKET", "instacart", "OSKOO", "BASIL", "HAMLE"],
        },
        "Tax + Benefits": ["TRUSTMARKBENEFIT"],
        "Yardim": ["WESTERN", "CKO*Patreon* Membershi"],
        "Credit cards": ["discover e-payment", "DISCOVER CO ENTRY", "american express", "chase card ending 2667",
                         "BARCLAYCARD us", "paypal", "CHASE CREDIT CRD"],
        "Ignore": ["Online Transfer to SAV|500"]
    }

    # Settings override
    from libs.helper import SETTINGS, Metric
    SETTINGS.METRICS = [Metric("Sum", sum)]  # Override metrics to only have Sum
    SETTINGS.LINE_LENGTH = 100
    SETTINGS.SHOW_EMPTY_CATEGORIES = False
    SETTINGS.SHOW_UNCATEGORIZED_SPENDINGS_AT_THE_END = True
    SETTINGS.SHOW_CATEGORY_METRICS = True
    SETTINGS.SHOW_CATEGORY_HEADER = True

    # Banks
    banks = [
        BankStatementInput(
            "Amex Preferred", "data/Feb7-Mar7/Amex-51004-activity.csv",
            "Amount", "Description", "Date"),
        BankStatementInput(
            "Amex Cash", "data/Feb7-Mar7/Amex-91003-activity.csv",
            "Amount", "Description", "Date"),
        BankStatementInput(
            "Chase Credit", "data/Feb7-Mar7/Chase2667_Activity20220307.CSV",
            "Amount", "Description", "Post Date", spending_shown_as_positive=False),
        BankStatementInput(
            "Chase Checking", "data/Feb7-Mar7/Chase7363_Activity_20220307.CSV",
            "Amount", "Description", "Posting Date", spending_shown_as_positive=False),
        BankStatementInput(
            "Discover", "data/Feb7-Mar7/Discover-RecentActivity-20220307.csv",
            "Amount", "Description", "Post Date"),
        BankStatementInput(
            "Paypal", "data/Feb7-Mar7/Paypal-Transaction.csv",
            "Amount", "Description", "Posting Date"),
        BankStatementInput(
            "Paypal", "data/Feb7-Mar7/Paypal-2-Transaction.csv",
            "Amount", "Description", "Posting Date"),
    ]
    budget_v2 = BudgetV2(break_down_details)
    budget_v2.run(banks)
