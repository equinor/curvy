import scipy
import datetime
import calendar
import numpy as np
from dateutil.relativedelta import relativedelta
import math

# Takes in the start date for the Day Ahead and converts in into a datetime with daily resolution.
def da_date(start_date):
    return datetime.date(start_date.year, start_date.month, start_date.day + 1)

# Takes in the start date for the Bound of Month and returns a list of all days remaining in the BOM.
def bom_dates(start_date):
    start_year, start_month, start_day = start_date.year, start_date.month, start_date.day + 2
    bom = []
    bom_days = calendar.monthrange(start_year, start_month)[1]
    for day in range(start_day, bom_days + 1):
        bom.append(datetime.date(start_year, start_month, day))
    return bom

# Takes in the start date for BOM and returns a list of all days in the first full month following BOM.
# If num_steps is larger than 1, the function will return a list of list containing each full month for
# each step defined in num_steps.
def eom_dates(start_date, num_steps):
    # Monthly
    eoms = []
    for i in range(1, num_steps + 1):
        current_eom = start_date + relativedelta(months=+i)
        eom_days = calendar.monthrange(current_eom.year, current_eom.month)[1]
        eom = []
        for day in range(1, eom_days + 1):
            eom.append(datetime.date(current_eom.year, current_eom.month, day))
        eoms.append(eom)
    return eoms

# Return the DA, BOM and EOM for a given number of steps.
# TODO: Implement other date systems.
def date_ranges(start_date, num_eoms, date_system='monthly'):
    # Day ahead
    da = da_date(start_date)
    # Bound of month
    bom = bom_dates(start_date)
    # eom
    eom = eom_dates(start_date, num_eoms)
    if ((start_date + relativedelta(days=+2)).month != start_date.month):
        return [[da]] + eom
    else:
        return [[da]] + [bom] + eom

# Copies the date range with equivalent ranges of price values
# Ex: prices_ranges([[1,2,3], [4,5,6]], [1,2])) -> [[1,1,1],[2,2,2]]
def price_ranges(date_ranges, forward_prices):
    if len(date_ranges) != len(forward_prices):
        raise ValueError('The number of date ranges and forwards prices need to be the same')
    y = []
    for i, date_range in enumerate(date_ranges):
        y.append([forward_prices[i]] * len(date_range))
    return y

# Flattens a 2D list with ranges into a 1D list of range values
# Ex: [[1,2],[3,4]] -> [1,2,3,4]
# If ranges are overlapping, set remove_overlap=True
# Ex: [[1,2,3],[3,4,5]] -> [1,2,3,4]
def flatten_ranges(ranges, no_overlap=False):
    if no_overlap:
        return [i for i in range(ranges[0][0], ranges[-1][-1])]
    else:
        return [item for sublist in ranges for item in sublist]

# Returns a list of the midpoint value in each range
# Ex: [[3, 5, 6], [3, 1, 8, 7]] -> [5, 8]
def midpoint_values(ranges, include_last=False):
    midpoints = []
    len_count = 0
    for r in ranges:
        mp_index = len(r) // 2
        midpoints.append(r[mp_index])
        len_count += len(r)
    if include_last:
        midpoints.append(ranges[-1][-1])
    return midpoints

# Returns the relative index to the midpoint of a range based on the start of the given range
# Ex: [[3, 5, 6, 3], [3, 1, 8, 7, 8]] -> [2, 2]
# TODO: Test with include last param
def midpoint_relative_index(ranges):
    relative_index = []
    len_count = 0
    for r in ranges:
        mp_index = len(r) // 2
        relative_index.append(mp_index)
        len_count += len(r)
    return relative_index

# Returns the absolute index to the midpoint, counted from the start of the first range
# Ex: [[3, 5, 6], [3, 1, 8, 7]] -> [1, 5]
# TODO: Test with include last param
def midpoint_absolute_index(ranges, include_last=False):
    absolute_index = []
    len_count = 0
    for r in ranges:
        mp_index = len(r) // 2
        absolute_index.append(len_count + mp_index)
        len_count += len(r)
    if include_last:
        absolute_index.append(len_count - 1)
    return absolute_index

# Returns the absolute start and end index for each range, counted from the start of the first range
# Ex: [[3, 5, 6], [3, 1, 8, 7]] -> [[0, 2], [3, 6]]
# With overlap=1, the function returns:
# Ex: [[3, 5, 6], [3, 1, 8, 7]] -> [[0, 3], [3, 7]]
def start_end_absolute_index(ranges, overlap=0):
    se_index = []
    len_count = 0
    for r in ranges:
        se_index.append([len_count, len_count + len(r) - 1 + overlap])
        len_count += len(r)
    return se_index

# Returns the index for each step between start and end for each range
# Ex: [[0, 2], [3, 7]] -> [[0, 1, 2], [3, 4, 5, 6, 7]]
def full_index(se_index):
    full_index = []
    len_count = 0
    for r in se_index:
        full_index.append([j for j in range(r[0], r[1] + 1)])
        len_count += len(r)
    return full_index

# Returns the middle value between two ranges for all ranges in a list of ranges
# Ex: [[1, 2],[2, 6], [6, 10]] -> [2, 6]
def knot_index(ranges):
    if len(ranges) < 2:
        raise ValueError('There must be at least 2 ranges in the list')
    knots = []
    for i in range(0, len(ranges[:-1])):
        knots.append((ranges[i][-1] + ranges[i + 1][0]) // 2)
    return knots

def get_ranges(start_date, prices):
    if len(prices) < 2:
        raise ValueError('The price list must contain at least 2 values')
    dr = date_ranges(start_date, len(prices) - 2)
    x = flatten_ranges(dr)
    pr = price_ranges(dr, prices)
    y = flatten_ranges(pr)
    return x, y, dr, pr
