import xlrd
import pandas
import spendings_calculations as sc
import spendings_data_reader as sdr

categories = pandas.read_excel("categories.xlsx")
tanechka_isracard = sdr.read_isracard_data("Export_3_2022.xls")
andrey_checkpoint = sdr.read_cal_data("Transactions_12_03_2022.xls")
tanechka_max = sdr.read_max_data("transaction-details_export_1660388403790.xlsx")

# spendings = pandas.concat([tanechka_isracard, andrey_checkpoint], ignore_index=True)
spendings = pandas.concat([tanechka_max], ignore_index=True)
total_result, result = sc.calculate_spendings_per_category(spendings, categories)

for key, val in total_result.items():
    print("{} - {:.2f}".format(key, val))

for key, val in result.items():
    print("{} - {}".format(key, val))