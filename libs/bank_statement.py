from enum import Enum
from typing import List, Tuple

from libs.transaction import Transaction


class FileType(Enum):
    CSV = ","
    TSV = "\t"


class BankStatementInput:
    name: str
    path: str
    file_type: FileType
    spending_shown_as_positive: bool
    amount_col_name: str
    description_col_name: str
    date_col_name: str

    def __init__(self, name: str, path: str, amount_col_name: str, description_col_name: str, date_col_name: str,
                 file_type: FileType = FileType.CSV, spending_shown_as_positive: bool = True):
        self.name = name
        self.path = path
        self.file_type = file_type
        self.spending_shown_as_positive = spending_shown_as_positive
        self.amount_col_name = amount_col_name
        self.description_col_name = description_col_name
        self.date_col_name = date_col_name


class BankStatement:
    name: str
    path: str
    spending_shown_as_positive: bool = False
    transactions: List[Transaction]

    __h: List[str]
    __d: List[List[str]]

    def __init__(self, bank_state_input: BankStatementInput):
        self.name = bank_state_input.name
        self.path = bank_state_input.path
        self.spending_shown_as_positive = bank_state_input.spending_shown_as_positive
        self.transactions = self.__parse_transactions(bank_state_input)

    def get_transactions(self):
        return self.transactions

    def __parse_transactions(self, bank_state_input: BankStatementInput) -> List[Transaction]:
        self.__h, self.__d = self.__read_file(bank_state_input.file_type)
        date_index = self.__h.index(bank_state_input.date_col_name)
        amount_index = self.__h.index(bank_state_input.amount_col_name)
        description_index = self.__h.index(bank_state_input.description_col_name)
        transactions = []
        for row in self.__d:
            transactions.append(
                Transaction(
                    date=row[date_index],
                    amount=row[amount_index],
                    description=row[description_index],
                    is_spending=(float(row[amount_index]) > 0) == self.spending_shown_as_positive,
                    bank=self.name
                )
            )
        return transactions

    def __read_file(self, file_type: FileType) -> Tuple[List[str], List[List[str]]]:
        h, d = [], []
        with open(self.path, 'r') as f:
            for line in f:
                row = [' '.join(cell.split()) for cell in line.split(str(file_type.value))]
                if not h:
                    h = [*row]
                else:
                    d.append([*row])
        return h, d
