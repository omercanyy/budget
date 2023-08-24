from __future__ import annotations

from typing import List, Dict, Union
from libs.helper import SETTINGS, format_str_with_fix_length, Alignment, Metric
from libs.transaction import Transaction


class Category:
    name: str
    group_by: str
    keywords: List[str]
    spendings: List[Transaction]

    def __init__(self, name: str, keywords: List[str], group_by=None):
        self.name = name
        self.spendings = []
        self.keywords = keywords
        self.group_by = group_by.upper() if group_by else name.upper()

    def add_spending(self, transaction: Transaction) -> None:
        self.spendings.append(transaction)

    def __repr__(self):
        category_header = self.__get_header()
        spendings = self.__get_spending_details()
        return f"{category_header}\n{spendings}"

    def get_category_summary(self) -> str:
        summary = [self.__get_spending_details()]

        if SETTINGS.SHOW_CATEGORY_HEADER:
            summary.insert(0, self.__get_header())

        if SETTINGS.SHOW_CATEGORY_METRICS:
            summary.append(self.__get_metrics())

        return '\n'.join(summary)

    def __get_header(self) -> str:
        return f"Category: {self.name}"

    def __get_spending_details(self) -> str:
        return '\n'.join(map(str, self.spendings))

    def __get_metrics(self):
        metrics = []
        for metric in SETTINGS.METRICS:
            metrics.append(
                format_str_with_fix_length(
                    f"(Sub-{metric.name}: ${self.__apply_metric(metric):,.2f})",
                    SETTINGS.LINE_LENGTH,
                    alignment=Alignment.right
                )
            )
        return '\n'.join(metrics)

    def __apply_metric(self, metric: Metric) -> Union[float, int]:
        return metric.run([s.amount for s in self.spendings])

    @classmethod
    def get_category_list_from_dict(cls, category_dict: Dict[str, Union[List[str], Dict[str, List[str]]]]) \
            -> List[Category]:
        category_list = []
        for k, v in category_dict.items():
            if isinstance(v, dict):
                for category_name, keywords in v.items():
                    category_list.append(cls(category_name, keywords, k))
            elif isinstance(v, list):
                category_list.append(cls(k, v, k))
            else:
                raise ValueError("Category dictionary you provided has syntax errors!")
        return category_list
