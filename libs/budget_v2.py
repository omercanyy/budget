from typing import List, Dict, Optional, Union
from math import ceil, floor

from libs.bank_statement import BankStatement, BankStatementInput
from libs.helper import SETTINGS, Alignment, format_str_with_fix_length, Metric
from libs.category import Category
from libs.transaction import Transaction


class BudgetV2:
    # transactions: List[Transaction]
    categories: List[Category]
    uncategorized = Category
    deposits = Category
    is_bank_statements_imported: bool

    def __init__(self, category_dict: Dict[str, Union[List[str], Dict[str, List[str]]]]):
        self.categories = Category.get_category_list_from_dict(category_dict)
        self.uncategorized = Category("Uncategorized", [])
        self.deposits = Category("Deposits", [])

    def run(self, bank_inputs: List[BankStatementInput], save_to_file: bool = False):
        transactions = [
            transaction
            for bank_input in bank_inputs
            for transaction in BankStatement(bank_input).get_transactions()
        ]
        self.categorize_spending(transactions)
        breakdown = self.get_breakdown()
        if save_to_file:
            with open('data/breakdown.csv', 'w') as f:
                f.write(breakdown)
        else:
            print(breakdown)

    def categorize_spending(self, transactions: List[Transaction]):
        num_of_transaction = len(transactions)

        for i in range(num_of_transaction):
            transaction = transactions.pop(0)

            if not transaction.is_spending:
                self.deposits.add_spending(transaction)

            if matched_category := self.__find_matching_category(transaction):
                matched_category.add_spending(transaction)
            else:
                self.uncategorized.add_spending(transaction)

    def get_breakdown(self):
        break_down_str = []

        # Group by
        group_by = {}
        for category in self.categories:
            if category.group_by not in group_by:
                group_by[category.group_by] = []
            group_by[category.group_by].append(category)

        # Append breakdown for each group_by
        for group_by_name in sorted(group_by.keys()):
            categories = group_by[group_by_name]
            if not categories or group_by_name.lower() == "ignore":
                continue

            # Margins
            total_margin = SETTINGS.LINE_LENGTH - len(group_by_name)
            left_margin = ceil(total_margin/2) - 1
            right_margin = floor(total_margin/2) - 1

            # Header
            break_down_str.append(("=" * left_margin) + f" {group_by_name} " + ("=" * right_margin))

            # Category
            for category in categories:
                if not category.spendings and not SETTINGS.SHOW_EMPTY_CATEGORIES:
                    continue
                break_down_str.append(category.get_category_summary())

            # Footer
            break_down_str.append('=' * SETTINGS.LINE_LENGTH)

            # Group by metric
            break_down_str.append(self.__get_group_by_metric(categories))

            # Empty line
            break_down_str.append("")

        if SETTINGS.SHOW_UNCATEGORIZED_SPENDINGS_AT_THE_END:
            break_down_str.append(self.show_uncategorized_spending())
        
        if SETTINGS.SHOW_DEPOSITS:
            break_down_str.append(self.show_deposits_spending())

        return '\n'.join(break_down_str)

    def show_uncategorized_spending(self):
        uncategorized_spending = [
            self.uncategorized.get_category_summary(),
            self.__get_group_by_metric([self.uncategorized])
        ]
        return '\n'.join(uncategorized_spending)
    
    def show_deposits_spending(self):
        deposits = [
            self.deposits.get_category_summary(),
            self.__get_group_by_metric([self.deposits])
        ]
        return '\n'.join(deposits)

    def __get_group_by_metric(self, categories: List[Category]):
        metrics = []
        for metric in SETTINGS.METRICS:
            metrics.append(format_str_with_fix_length(
                f"{metric.name}: ${self.__calc_group_by_metric(metric, categories):,.2f}",
                SETTINGS.LINE_LENGTH,
                alignment=Alignment.right
            ))
        return '\n'.join(metrics)

    def __find_matching_category(self, transaction: Transaction) -> Optional[Category]:
        for category in self.categories:
            for keyword in category.keywords:
                if self.__is_keyword_and_transaction_match(keyword, transaction):
                    return category
        return None

    @staticmethod
    def __calc_group_by_metric(metric: Metric, categories: List[Category]) -> Union[float, int]:
        return metric.run([s.amount for category in categories for s in category.spendings])

    @staticmethod
    def __is_keyword_and_transaction_match(keyword: str, transaction: Transaction) -> bool:
        is_keyword_match = keyword.split("|")[0].lower() in transaction.description.lower()
        is_amount_match = keyword.split("|")[1] in str(transaction.amount) if "|" in keyword else True
        return is_keyword_match and is_amount_match
