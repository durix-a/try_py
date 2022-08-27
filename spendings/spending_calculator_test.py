import pytest
import spendings_calculations as sc
import spendings_data_reader as sdr
import pandas


class TestSpendingsCalculator:
    def test_categories_matching(self):
        date_list = ["01/01/2022", "02/01/2022", "03/01/2022", "04/01/2022", "05/01/2022", "06/01/2022"]
        business_list = ["shoe maker", "installator", "carpenter", "peice maker", "aggragator", "mechanic"]
        sum_list = [20.1, 199.9, 55.5, 20.11, 199.91, 55.51]
        spendings = pandas.DataFrame({sdr.DATE_COLUMN_LABEL:date_list, sdr.BUSINESS_COLUMN_LABEL:business_list, sdr.PAIED_SUM_COLUMN_LABEL:sum_list})

        business_pattern_list = [".* maker", ".*ator", "carpenter", "mechanic"]
        category_list = ["cat1", "cat2", "cat3", "cat3"]
        type_list = ["pattern", "pattern", "string", "string"]
        categories = pandas.DataFrame({"business_name":business_pattern_list, "category_name":category_list, "type":type_list})

        spendings_calculator = sc.SpendingsCalculator(categories)
        result = spendings_calculator.calculate_spendings_per_category(spendings)
        
        cat1_data = result["cat1"]
        assert cat1_data.shape == (3, 3)
        assert "01/01/2022" == cat1_data.loc[0].date
        assert "shoe maker" == cat1_data.loc[0].business
        assert 20.1 == cat1_data.loc[0].paied_sum
        assert "04/01/2022" == cat1_data.loc[1].date
        assert "peice maker" == cat1_data.loc[1].business
        assert 20.11 == cat1_data.loc[1].paied_sum
        
        cat2_data = result["cat2"]
        assert cat2_data.shape == (3, 3)
        assert "02/01/2022" == cat2_data.loc[0].date
        assert "installator" == cat2_data.loc[0].business
        assert 199.9 == cat2_data.loc[0].paied_sum
        assert "05/01/2022" == cat2_data.loc[1].date
        assert "aggragator" == cat2_data.loc[1].business
        assert 199.91 == cat2_data.loc[1].paied_sum
        
        cat3_data = result["cat3"]
        assert cat3_data.shape == (3, 3)
        assert "03/01/2022" == cat3_data.loc[0].date
        assert "carpenter" == cat3_data.loc[0].business
        assert 55.5 == cat3_data.loc[0].paied_sum
        assert "06/01/2022" == cat3_data.loc[1].date
        assert "mechanic" == cat3_data.loc[1].business
        assert 55.51 == cat3_data.loc[1].paied_sum
