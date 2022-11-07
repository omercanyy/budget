from libs.helper import SETTINGS, Alignment, format_str_with_fix_length, convert_amount_to_float


class Transaction:
    description: str
    amount: float
    date: str
    is_spending: bool
    bank: str

    def __init__(self, description: str, amount: str, date: str, is_spending: bool, bank: str):
        self.description = description
        self.amount = convert_amount_to_float(amount)
        self.date = date
        self.is_spending = is_spending
        self.bank = bank

    def __repr__(self):
        # Lengths
        date_len = 13
        amount_len = 11
        bank_len = 15
        description_len = max((SETTINGS.LINE_LENGTH - date_len - amount_len - bank_len), 20)

        # Date
        date = self.date
        amount = f"${self.amount:,.2f}"
        bank = self.bank[:bank_len - 2]
        description = f"{self.description[:(description_len-4)]}..." \
            if len(self.description) > (description_len-4) \
            else self.description

        # Data
        date_str = format_str_with_fix_length(date, date_len, alignment=Alignment.left)
        amount_str = format_str_with_fix_length(amount, amount_len, alignment=Alignment.right)
        bank_str = format_str_with_fix_length(bank, bank_len, alignment=Alignment.right)
        description_str = format_str_with_fix_length(description.replace('"', ""), description_len, alignment=Alignment.left)

        return f"{date_str}{description_str}{amount_str}{bank_str}"
