import os
import pandas as pd
from pandas import DataFrame
from report import Report
import math


class OldImportReport(Report):

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['serialNum', 'amount', 'avgCost', 'importPrice']
        self.SELECTED_COL_IDS = r'C, E, F, G'

    def importExcelSheet(self):
        if not os.path.isfile(self.metadata_filename):
            print(f"file {self.metadata_filename} doesn't exists")
            return
        df_metadata = pd.read_excel(self.metadata_filename, header=None, skiprows=[0, 1, 2],
                                    usecols=self.SELECTED_COL_IDS,
                                    names=self.SELECTED_COL_NAMES,
                                    converters=self.CONVERTERS
                                    )
        return df_metadata

    def convertTextDataToDigital(self, df):
        df[self.SELECTED_COL_NAMES[1]] = df[self.SELECTED_COL_NAMES[1]].map(self.parseAmount)
        for i in [2, 3]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parsePrice)
        return df

    def compareDicts(self, dict_old, dict_new):
        if dict_old.size != dict_new.size:
            return False
        bool_arr = (dict_old.values == dict_new.values)
        for i in [1, 2, 3]:
            if not bool_arr[0][i]:
                return False
        return True
