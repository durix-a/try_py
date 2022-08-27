import xlrd
import pandas
import spendings_calculations as sc
import spendings_data_reader as sdr

categories = pandas.read_excel("categories.xlsx")
# tanechka_isracard = sdr.read_isracard_data("Export_3_2022.xls")
# andrey_checkpoint = sdr.read_cal_data("Transactions_12_03_2022.xls")
# tanechka_max = sdr.read_max_data("transaction-details_export_1660388403790.xlsx")

# spendings = pandas.concat([tanechka_isracard, andrey_checkpoint], ignore_index=True)
# spendings = pandas.concat([tanechka_max], ignore_index=True)
spendings = sdr.scan_folder_for_data("2022-08")
spendings_calculator = sc.SpendingsCalculator(categories)
result = spendings_calculator.calculate_spendings_per_category(spendings)

# for key, val in result.items():
#     print("{} - {}".format(key, val))

with pandas.ExcelWriter('output.xlsx') as writer:
    for key, val in result.items():
        if(key):
            val.to_excel(writer, sheet_name=key)
        else:
            val.to_excel(writer, sheet_name="хз")
