#!/usr/bin/python
# -*- coding: UTF-8 -*-
import math

from pandas import DataFrame

from report import Report


class OldExportReport(Report):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['supplierName', 'categoryName', 'serialNum', 'saleAmount', 'saleTotal',
                                   'totalCost', 'grossProfit', 'grossProfitRate']
        self.SELECTED_COL_IDS = r'C, D, F, H, I, J, K, L'

        self.COMPARE_COLS = [2, 3, 4, 5, 8]

    def cleanTable(self, df, col_idx_serial_no):
        cleaned_df = DataFrame()
        for i in range(len(df)):
            row = df.loc[i, :]
            col_name_serial_num = self.SELECTED_COL_NAMES[col_idx_serial_no]
            # clean empty row
            try:
                if math.isnan(row[col_name_serial_num]):
                    continue
            except TypeError:
                if self.isSerialNum(row[col_name_serial_num]):
                    # clean united sale
                    if len(row[col_name_serial_num]) != 5:
                        #  祥坤蔬菜店商品为联营
                        if row["supplierName"] != "祥坤蔬菜":
                            cleaned_df = cleaned_df.append(row)
        return cleaned_df

    def convertTextDataToDigital(self, df):
        for i in [3]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parseAmount)
        for i in [4, 5, 6]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parsePrice)
        return df
