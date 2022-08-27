import pandas
import spendings_data_reader as sdr
import re


class SpendingsCategoryBusinessPair:
    def __init__(self, name, business_comparator):
        self.name = name
        self.business_comparator = business_comparator

    def is_bussiness_match(self, business_name):
        if(isinstance(self.business_comparator, str)):
            if(self.business_comparator.casefold() == business_name.casefold()):
                return True
        elif(isinstance(self.business_comparator, re.Pattern)):
            matched_business_name = self.business_comparator.search(business_name)
            if(matched_business_name):
                return True

        return False

class SpendingsCalculator:
    def __init__(self, categories_list : pandas.DataFrame):
        self.categories = []

        for row_iter in categories_list.iterrows():
            row = row_iter[1]
            if(row.type == "string"):
                self.categories.append(SpendingsCategoryBusinessPair(row.category_name, row.business_name))
            elif(row.type == "pattern"):
                self.categories.append(SpendingsCategoryBusinessPair(row.category_name, re.compile(row.business_name)))

    def __find_category(self, business_name : str):
        for category_business_pair in self.categories:
            if(category_business_pair.is_bussiness_match(business_name)):
                return category_business_pair.name
        
        return None

    def calculate_spendings_per_category(self, spendings : pandas.DataFrame):
        total_spendings_per_category = {"total": 0}
        spendings_per_category = {}

        for row_iter in spendings.iterrows():
            row = row_iter[1]
            category_name = self.__find_category(row.business)
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
