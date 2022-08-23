import pandas
import spendings_data_reader as sdr

def find_category(business_name, categories : pandas.DataFrame):
    for row in categories.itertuples():
        if(business_name.casefold() == row[1].casefold()):
            return row[2]
    
    return None

def calculate_spendings_per_category(spendings : pandas.DataFrame, categories_list : pandas.DataFrame):
    total_spendings_per_category = {"total": 0}
    spendings_per_category = {}

    for row_iter in spendings.iterrows():
        row = row_iter[1]
        category_name = find_category(row.business, categories_list)
        spent_sum = row.paied_sum

        if(category_name not in total_spendings_per_category):
            total_spendings_per_category[category_name] = 0
            spendings_per_category[category_name] = pandas.DataFrame(columns=[sdr.DATE_COLUMN_LABEL, sdr.BUSINESS_COLUMN_LABEL, sdr.PAIED_SUM_COLUMN_LABEL])
        
        total_spendings_per_category[category_name] = total_spendings_per_category[category_name] + spent_sum
        total_spendings_per_category["total"] = total_spendings_per_category["total"] + spent_sum
        spendings_category = spendings_per_category[category_name]
        spendings_category.loc[spendings_category.shape[0]] = row

    for category_name, spendings_category in spendings_per_category.items():
        spendings_category.loc[spendings_category.shape[0]] = ["", "total", total_spendings_per_category[category_name]]

    total_spendings = pandas.DataFrame(columns=["category", "total sum"])
    for category_name, total_sum in total_spendings_per_category.items():
        total_spendings.loc[total_spendings.shape[0]] = [category_name, total_sum]


    spendings_per_category["total"] = total_spendings
    return spendings_per_category
