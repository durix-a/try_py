import xlrd
import pandas
import re
import os

DATE_COLUMN_LABEL = "date"
BUSINESS_COLUMN_LABEL = "business"
PAIED_SUM_COLUMN_LABEL = "paied_sum"

def is_isracard_row_skiped(row):
    return row[6].ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK) or not row[6].value

def get_isracard_data_indeces(row):
    sum_index = business_index = date_index = index = 0

    for cell in row:
        if(cell.value == "תאריך רכישה"):
            date_index = index
        elif(cell.value == "שם בית עסק"):
            business_index = index
        elif(cell.value == "סכום חיוב"):
            sum_index = index
        
        index = index + 1

    return date_index, business_index, sum_index


def read_isracard_data(filename):
    book = xlrd.open_workbook(filename)
    # print("The number of worksheets is {0}".format(book.nsheets))
    # print("Worksheet name(s): {0}".format(book.sheet_names()))
    sh = book.sheet_by_index(0)
    # print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
    # print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
    # count = 15

    date_list = []
    date_column_index = 0
    business_list = []
    business_column_index = 1
    sum_list = []
    sum_column_index = 4

    for row in sh.get_rows():
        if(is_isracard_row_skiped(row)):
            continue

        #print("{}, {}, {} - {} - {}".format(row[0].value, row[1].value, row[4].value, len(row), row[6]))
        if(row[0].value == "תאריך רכישה"):
            date_column_index, business_column_index, sum_column_index = get_isracard_data_indeces(row)
            continue

        date_list.append(row[date_column_index].value)
        business_list.append(row[business_column_index].value)
        sum_list.append(row[sum_column_index].value)

    return pandas.DataFrame({DATE_COLUMN_LABEL:date_list, BUSINESS_COLUMN_LABEL:business_list, PAIED_SUM_COLUMN_LABEL:sum_list})

def convert_cal_sum(sum_value):
    spent_sum_numeric = re.search("[0-9,\\.-]+", sum_value)
    spent_sum_numeric = spent_sum_numeric.group(0).replace(",", "")
    return float(spent_sum_numeric)

def read_cal_data(filename):
    return pandas.read_csv(filename, encoding="utf-16", sep="\t", skiprows=2, skipfooter=1, engine="python", header=0, names=[DATE_COLUMN_LABEL, BUSINESS_COLUMN_LABEL, PAIED_SUM_COLUMN_LABEL], usecols=[0, 1, 3], converters={PAIED_SUM_COLUMN_LABEL:convert_cal_sum})

def read_max_data(filename):
    return pandas.read_excel(filename, sheet_name="עסקאות במועד החיוב", skiprows=4, skipfooter=3, header=None, names=[DATE_COLUMN_LABEL, BUSINESS_COLUMN_LABEL, PAIED_SUM_COLUMN_LABEL], usecols=[0, 1, 5])

def scan_folder_for_data(folderPath):
    filenames_list = next(os.walk(folderPath), (None, None, []))[2]

    for filename in filenames_list:
        matched_file = re.search("Export_[0-9]{1,2}_[0-9]{4}\.xls", filename)
        if(matched_file[0]):
            read_isracard_data