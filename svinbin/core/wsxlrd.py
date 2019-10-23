from xlrd import open_workbook, xldate_as_tuple
import re
import datetime


def init_wb(filepath):
    wb = open_workbook(filepath)
    return wb


def normalize_row(row, workbook):
    row[0] = int(row[0]) # farm_id to int
    row[4] = datetime.datetime(*xldate_as_tuple(row[4], workbook.datemode)) # date to dttime
    if row[5] == '*' or row[5] == '**':
        del row[5] # delete *
    row[5] = int(row[5])
    row[7] = int(row[7])

    return row


def define_match_row_and_convert_datetime(row_values):
    if len(row_values) > 3 and \
        re.match(r'^[0-9]+$', str(row_values[0])) and \
        re.match(r'^[0-9A-Z]+$', str(row_values[1])) and \
        re.match(r'^[0-9]{4}$', str(row_values[3])):        
        return True
        
    return False


def get_semenation_rows(workbook):
    rows = list()
    for s in workbook.sheets():
        for row in range(s.nrows):
            row_values = list()
            for col in range(s.ncols):
                if len(str(s.cell(row,col).value).strip()) > 0:
                    row_values.append(s.cell(row, col).value)
            if define_match_row_and_convert_datetime(row_values):
                row_values = normalize_row(row_values, workbook)
                rows.append(row_values)
    return rows