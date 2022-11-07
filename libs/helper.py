from typing import List, Callable, Union


class Alignment:
    left = "L"
    right = "R"


def format_str_with_fix_length(s: str, length: int, alignment: Alignment = Alignment.left):
    if len(s) > length:
        s = s[:length]
    aligned_str = [" "] * length
    for i in range(len(s)):
        if i < length:
            if alignment == Alignment.left:
                aligned_str[i] = s[i]
            elif alignment == Alignment.right:
                aligned_str[-i - 1] = s[-i - 1]
            else:
                raise ValueError(f"No such alignment implementation for '{alignment}'")
            # aligned_str[i if left_alignment else -i - 1] = s[i if left_alignment else -i - 1]
    return ''.join(aligned_str)


def convert_amount_to_float(amount: str):
    # Convert to float
    amount_float = float(amount)

    # Convert to positive
    if amount_float < 0:
        amount_float = -amount_float

    return amount_float


class Metric:
    name: str
    __executable: Callable

    def __init__(self, name: str, executable: Callable):
        self.name = name
        self.__executable = executable

    def run(self, nums: List[Union[int, float]]) -> int:
        return self.__executable(nums)


class Settings:
    # BANK_HEADER_FILLING: int
    # SHOW_PREVIEW_WHEN_FILE_IS_READ: bool
    # SHOW_DETAILED_BREAK_DOWN: bool
    # SHOW_SPENDING_PATTERN_GRAPHS: bool
    # CASE_SENSITIVE_SEARCH: bool
    SHOW_CATEGORY_NAME: bool
    SHOW_CATEGORY_SUM: bool
    SHOW_UNCATEGORIZED_SPENDINGS_AT_THE_END: bool
    SHOW_EMPTY_CATEGORIES: bool
    LINE_LENGTH: int
    METRICS: List[Metric]

    def default(self):
        # self.BANK_HEADER_FILLING = 25
        # self.SHOW_PREVIEW_WHEN_FILE_IS_READ = False
        # self.SHOW_DETAILED_BREAK_DOWN = True
        # self.SHOW_SPENDING_PATTERN_GRAPHS = False
        # self.CASE_SENSITIVE_SEARCH = False
        self.SHOW_CATEGORY_NAME = False
        self.SHOW_CATEGORY_SUM = False
        self.SHOW_UNCATEGORIZED_SPENDINGS_AT_THE_END = False
        self.SHOW_EMPTY_CATEGORIES = True
        self.LINE_LENGTH = 70

        from statistics import mean, median
        self.METRICS = [
            Metric("Sum", sum),
            Metric("Average", mean),
            Metric("Median", median)]
        return self

    def __repr__(self):
        return '\n'.join(f"{k}: {v}" for k, v in self.__dict__.items())


SETTINGS = Settings().default()
