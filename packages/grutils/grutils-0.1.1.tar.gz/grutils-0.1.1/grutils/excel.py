#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from xlwings.utils import rgb_to_int

from .error import Error
import xlwings as xw


def sheet_with_name(err: Error, wb: xw.Book, name='sheet name'):
    if err.has_error():
        return None
    for sht in wb.sheets:
        if sht.name == name:
            return sht

    err.append('excel file({}) has no sheet named "{}"'.format(wb.fullname, name))
    return None


def count_of_continue_none_cells(items: List[any] = None):
    if items is None:
        items = []
    i = len(items) - 1
    count = 0
    while i >= 0:
        if items[i] is None:
            count += 1
        else:
            break
        i -= 1
    return count


def row_items(err: Error, sht: xw.Sheet, row=1, first_column='A', last_column='ZZ'):
    if err.has_error():
        return None
    range_str = '{}{}:{}{}'.format(first_column, row, last_column, row)
    r = sht.range(range_str)
    cells = r.value

    count = count_of_continue_none_cells(cells)
    return cells[0:len(cells) - count]


def row_items_with_column(err: Error, sht: xw.Sheet, row=1, first_column='A', last_column='ZZ'):
    items = row_items(err, sht, row, first_column, last_column)
    results = []
    i = 0
    for item in items:
        results.append((add_column(first_column, i), item))
        i += 1

    return results


def row_items_filtered(err: Error, sht: xw.Sheet, tester=lambda x: True, row=1, first_column='A', last_column='ZZ'):
    items = row_items_with_column(err, sht, row, first_column, last_column)
    if tester is None:
        return items

    results = filter(lambda x: tester(x[1]), items)
    return list(results)


def column_items_sub(err: Error, sht: xw.Sheet, column='A', start_row=1, steps=100):
    if err.has_error():
        return []
    end_row = start_row + steps - 1
    if type(column) == str:
        range_str = '{}{}:{}{}'.format(column, start_row, column, end_row)
        return sht.range(range_str).value
    else:
        return sht.range((start_row, column), (end_row, column)).value


def column_items(err: Error, sht: xw.Sheet, column='A', start_row=1, steps=100):
    if err.has_error():
        return []

    items = []
    start_row_sub = start_row
    count = count_of_continue_none_cells(items)
    while count < 20:
        items = items + column_items_sub(err, sht, column, start_row_sub, steps)
        start_row_sub += steps
        count = count_of_continue_none_cells(items)

    return items[0:len(items) - count]


def column_items_with_row(err: Error, sht: xw.Sheet, column='A', start_row=1, steps=100):
    items = column_items(err, sht, column, start_row, steps)
    results = []
    i = 0
    for item in items:
        results.append((start_row + i, item))
        i += 1

    return results


def column_items_filtered(err: Error, sht: xw.Sheet, tester=lambda x: True, column='A', start_row=1, steps=100):
    items = column_items_with_row(err, sht, column, start_row, steps)
    if tester is None:
        return items

    results = filter(lambda x: tester(x[1]), items)
    return list(results)


def num_to_column(num: int):
    if num < 0:
        s = 'column number({}) is less than 0'.format(num)
        raise Exception(s)
    elif num == 0:
        return ""
    elif num <= 26:
        return chr(65 - 1 + num)

    right = num % 26
    if right == 0:
        right = 26
    left = int((num - right) / 26)
    return num_to_column(left) + num_to_column(right)


def column_to_num(column: str):
    length = len(column)
    if length == 0:
        return 0
    elif length == 1:
        num = ord(column.upper()) - ord('A') + 1
        if num < 1 or num > 26:
            s = 'column char({}) is not in a~z, or A~Z'.format(column)
            raise Exception(s)
        return num
    else:
        return 26 * column_to_num(column[0:length - 1]) + column_to_num(column[length - 1:])


def add_column(column: str, add_num: int):
    num = column_to_num(column)
    return num_to_column(num + add_num)


def close_wb(wb: xw.Book):
    if wb is not None:
        wb.close()


def quit_app(app: xw.App):
    if app is not None:
        app.quit()


def orange_red():
    return rgb_to_int((255, 69, 0))


def banana_yellow():
    return rgb_to_int((227, 207, 87))


def sky_blue():
    return rgb_to_int((135, 206, 235))


def green():
    return rgb_to_int((0, 255, 0))
