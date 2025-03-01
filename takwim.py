# this is a POC for single page calendar
# list all days in the year 
# group months that start on the same day of the week
# print the calendar

import calendar
import datetime
from collections import defaultdict
from typing import Any, Callable, TypeVar
import sys

# make YEAR passed via argv
if len(sys.argv) < 2:
    YEAR = datetime.datetime.now().year
else:
    YEAR = int(sys.argv[1])


V = TypeVar('V')
R = TypeVar('R')

def matrix_map(func: Callable[[V],R], matrix: list[list[V]]) -> list[list[R]]:
    return [[func(val) for val in row] for row in matrix]

def matrix_transpose(matrix: list[list[V]]) -> list[list[V]]:
    return list(map(list, zip(*matrix)))

def group_months_by_start_day(year: int) -> dict[int, list[int]]:
    # in a dict store months that start on the same day of the week
    # key is the day of the week and value is a list of months
    months_grouped_start = defaultdict(list)
    for month in range(1, 13):
        month_start_day = calendar.weekday(year, month, 1)
        # change name of the month from number to its name
        months_grouped_start[month_start_day].append(month)

    # maximum 3 months should start on the same day of the week
    assert max(len(v) for v in months_grouped_start.values()) < 4
    # sorted by the day of the week. (i.e. the 1st month always start on Monday)
    return dict(sorted(months_grouped_start.items()))

# print the months like so:
# Sep Apr Jan May Aug Feb Jun
# Dec Jul Oct         Mar
#                     Nov

# make a matrix and fill the months in it
# [day][index]
months_matrix: list[list[int | None]] = [[] for i in range(7)]
for day, months in group_months_by_start_day(YEAR).items():
    for month in months:
        months_matrix[day].append(month)

# fill remaining values in months_matrix with None
for i in range(7):
    while len(months_matrix[i]) < 3:
        months_matrix[i].append(None)

# reverse the matrix 
months_matrix = matrix_transpose(months_matrix)

# apply following value on matrix
# calendar.month_name[month][:3]
def get_month_name(month: int | None) -> str | None:
    if month is None:
        return None
    return calendar.month_name[month][:3]
    
named_months_matrix = matrix_map(get_month_name, months_matrix)


# print the months calendar
# if the month is None print empty space
# transform the int representing the month to 3 letter string representing the month
def render_matrix(matrix: list[list[Any]], min_chars: int) -> list[str]:
    assert_matrix(matrix)
    result = []
    for row in matrix:
        row_str = ""
        for val in row:
            if val is None:
                row_str += f"{'':>{min_chars}} "
            else:
                row_str += f"{val:>{min_chars}} "
        result.append(row_str)
    return result

def assert_matrix(matrix: list[list[V]]) -> None:
    for row in matrix[1:]:
        assert len(row) == len(matrix[0])

def concat_matrices(matrix_left: list[str], matrix_right: list[str]) -> list[str]:
    """Put two matrices side by side."""
    return [left+right for left, right in zip(matrix_left, matrix_right, strict=True)]
    


def print_matrix(matrix: list[str]) -> None:
    for row in matrix:
        print(row)

### DEBUG ###
# print_matrix(render_matrix(named_months_matrix, 3)   )

# make a matrix containing all days in a 31 day month
# it should be 7x5 matrix
# fill the days in the matrix
# start with 1 
# if the day is greater than 31 fill with None

days_months: list[list[int|None]] = [
    [1, 8, 15, 22, 29],
    [2, 9, 16, 23, 30],
    [3, 10, 17, 24, 31],
    [4, 11, 18, 25, None],
    [5, 12, 19, 26, None],
    [6, 13, 20, 27, None],
    [7, 14, 21, 28, None],
]

### DEBUG ###
# print_matrix(render_matrix(days_months, 2))

days_of_week = [
    "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
]
# days of week combinations is obtained by rotating the days_of_week 7 times
days_of_week_combinations = [days_of_week[i:] + days_of_week[:i] for i in range(7)]

### DEBUG ###
# print_matrix(render_matrix(days_of_week_combinations, 3))

# using * 3 because days_months is 2 chars wide + 1 space
top_empty_part_matrix = [" "*len(days_months[0]) * 3] * len(named_months_matrix)
top_part = concat_matrices(top_empty_part_matrix, render_matrix(named_months_matrix, 3))

bottom_part = concat_matrices(render_matrix(days_months, 2), render_matrix(days_of_week_combinations, 3))


# header of the calendar
print(f"Year {YEAR} Calendar\n")
print_matrix(top_part)
print_matrix(bottom_part)
