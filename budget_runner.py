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
            "Mortgage": ["Navigate Propert", "MORTGAGE COMPANY"],
            "Personal Loan": ["Best Egg|1130"],
            "Energy": ["seattle city lights", "SEATTLE CITY LIGHT", "SNOHOMISH COUNTY PUD"],
        },
        "Transportation": {
            "Car": ["BECU"],
            "Car Insurance": ["PROG DIRECT INS  INS PREM", "PROG DIRECT INS"],
            "Gas": ["CHEVRON", "SHELL", "SAFEWAY FUEL"],
            "Tolls": ["GOODTOGO"]
        },
        "Bills": {
            "Internet": ["COMCAST CABLE COMM", "comcast"],
            "Streaming": ["Prime Video", "peacock", "disney", "hulu", "spotify"],
            "Phone": ["Zelle payment to Omer Faruk Aslan"],
            "Other": ["labcor", "public storage", "safe deposit box", "educative", "PLANET FIT CLUB", "CHATGPT", "CloudwaysLTD"],
        },
        "Food + Groceries": {
            "Eating Out + Catering": ["DOORDASH", "DUTCH BROS", "Starbucks", "fresh flours", "common ground coffee", 
                                    "PARADISE RESTAURAN SEATTLE", "SHAKE SHACK", "BEQUEST", "SKYVIEW", "COPPERLEAF", 
                                    "LA SABROSA", "LA COSTA", "CAFE SABAH", "OLIVE GARDEN", "BLAZING BAGELS", "IHOP",
                                    "URBAN CITY COFFEE", "CASTELLO", "PIZZA HUT", "CHEESECAKE"],
            "Groceries": ["FRED MEYER", "DK MARKET", "instacart", "OSKOO", "BASIL", "HAMLE"],
        },
        "Tax + Benefits": ["TRUSTMARKBENEFIT"],
        "Yardim": {
            "Tevhide": ["WESTERN|200"],
            "Ridvan": ["Patreon* Membershi"],
            "Kubra": ["kubra"],
            "Other": ["WESTERN"]
        },
        "Credit cards": ["discover e-payment", "DISCOVER CO ENTRY", "american express", "chase card ending 2667",
                         "BARCLAYCARD us", "paypal", "CHASE CREDIT CRD"],
        "Other": ["CLEARME.COM", "Best Egg|1154", "Zelle payment to Faruk Ogrenci", "APPLECARD GSBANK", "ATM WITHDRAWAL", 
                "Zelle payment to Ahmet Bulut", "NASH POWERSPORTS"]
    }

    # Settings override
    from libs.helper import SETTINGS, Metric
    SETTINGS.METRICS = [Metric("Sum", sum)]  # Override metrics to only have Sum
    SETTINGS.LINE_LENGTH = 100
    SETTINGS.SHOW_EMPTY_CATEGORIES = False
    SETTINGS.SHOW_UNCATEGORIZED_SPENDINGS_AT_THE_END = True
    SETTINGS.SHOW_DEPOSITS = True
    SETTINGS.SHOW_CATEGORY_METRICS = True
    SETTINGS.SHOW_CATEGORY_HEADER = True

    # Banks
    banks = [
        BankStatementInput(
            "Chase Checking Personal", "data/Jun20_Aug20/Chase7363_Activity_20230820.CSV",
            "Amount", "Description", "Posting Date", spending_shown_as_positive=False),
        BankStatementInput(
            "Chase Checking Personal", "data/Jun20_Aug20/Chase9553_Activity_20230820.CSV",
            "Amount", "Description", "Posting Date", spending_shown_as_positive=False),
        BankStatementInput(
            "Chase Credit", "data/Jun20_Aug20/Chase2667_Activity20230620_20230820_20230820.CSV",
            "Amount", "Description", "Post Date", spending_shown_as_positive=False),
        BankStatementInput(
            "Amex Preferred", "data/Jun20_Aug20/Amex_Preferred_Jun20_Aug20_activity.csv",
            "Amount", "Description", "Date"),
        BankStatementInput(
            "Amex Cash", "data/Jun20_Aug20/Amex_Cash_Jun20_Aug20_activity.csv",
            "Amount", "Description", "Date"),
        BankStatementInput(
            "Discover", "data/Jun20_Aug20/DFS-Search-20230820.csv",
            "Amount", "Description", "Post Date"),
    ]
    budget_v2 = BudgetV2(break_down_details)
    budget_v2.run(banks) # save_to_file=True to save the breakdown into data/breakdown.csv
