import xlrd
import pandas
import re
import os
import enum

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

class CalSumConverter:
    def __init__(self):
        self.compiled_converter_pattern = re.compile("[0-9,\\.-]+")

    def __call__(self, sum_value):
        spent_sum_numeric = self.compiled_converter_pattern.search(sum_value)
        spent_sum_numeric = spent_sum_numeric.group(0).replace(",", "")
        return float(spent_sum_numeric)

def read_cal_data(filename):
    returned_data = pandas.read_csv(filename, encoding="utf-16", sep="\t", skiprows=2, skipfooter=1, engine="python", header=0, usecols=["תאריך העסקה", "שם בית העסק", "סכום החיוב"], converters={"סכום החיוב":CalSumConverter()})
    returned_data.columns = [DATE_COLUMN_LABEL, BUSINESS_COLUMN_LABEL, PAIED_SUM_COLUMN_LABEL]
    return returned_data

def read_max_data(filename):
    return pandas.read_excel(filename, sheet_name="עסקאות במועד החיוב", skiprows=4, skipfooter=3, header=None, names=[DATE_COLUMN_LABEL, BUSINESS_COLUMN_LABEL, PAIED_SUM_COLUMN_LABEL], usecols=[0, 1, 5])

class SPENDINGS_DATA_TYPE(enum.Enum):
    OTHER = 0
    CAL = 1
    ISRACARD = 2
    MAX = 3

def filename_to_data_type(filename):
    matched_file = re.search("Export_[0-9]{1,2}_[0-9]{4}\.xls", filename)
    if(matched_file and matched_file[0] == filename):
        return SPENDINGS_DATA_TYPE.ISRACARD
    
    matched_file = re.search("Transactions_[0-9]{2}_[0-9]{2}_[0-9]{4}.*\.xls", filename)
    if(matched_file and matched_file[0] == filename):
        return SPENDINGS_DATA_TYPE.CAL
    
    matched_file = re.search("transaction-details_export_[0-9]*\.xlsx", filename)
    if(matched_file and matched_file[0] == filename):
        return SPENDINGS_DATA_TYPE.MAX

    return SPENDINGS_DATA_TYPE.OTHER

def scan_folder_for_data(folderPath):
    filenames_list = next(os.walk(folderPath), (None, None, []))[2]
    folder_data = pandas.DataFrame(columns=[DATE_COLUMN_LABEL, BUSINESS_COLUMN_LABEL, PAIED_SUM_COLUMN_LABEL])
    data_readers_map = { SPENDINGS_DATA_TYPE.CAL : read_cal_data, 
                         SPENDINGS_DATA_TYPE.ISRACARD : read_isracard_data, 
                         SPENDINGS_DATA_TYPE.MAX : read_max_data }

    for filename in filenames_list:
        spendings = None
        data_type = filename_to_data_type(filename)
        filepath = os.path.join(folderPath, filename)
        print("found {} file {}".format(data_type, filepath))

        if(data_type != SPENDINGS_DATA_TYPE.OTHER):
            spendings = data_readers_map[data_type](filepath)
            folder_data = pandas.concat([folder_data, spendings], ignore_index=True)
    
    return folder_data