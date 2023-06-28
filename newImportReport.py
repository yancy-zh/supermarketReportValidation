import os

import pandas as pd

from report import Report


class NewImportReport(Report):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['serialNum', 'avgCost', 'amount', 'importPrice']
        self.SELECTED_COL_IDS = r'K, Q, S, T'

    def importExcelSheet(self):
        if not os.path.isfile(self.metadata_filename):
            print(f"file {self.metadata_filename} doesn't exists")
            return
        df_metadata = pd.read_excel(self.metadata_filename, header=None, skiprows=[0, 1, 2, 3, 4, 5],
                                    usecols=self.SELECTED_COL_IDS,
                                    names=self.SELECTED_COL_NAMES,
                                    converters=self.CONVERTERS
                                    )
        return df_metadata

    def convertTextDataToDigital(self, df):
        df[self.SELECTED_COL_NAMES[2]] = df[self.SELECTED_COL_NAMES[2]].map(self.parseAmount)
        for i in [1, 3]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.roundPrice)
        return df