#!/usr/bin/python
# -*- coding: UTF-8 -*-
import math

from pandas import DataFrame

from report import Report


class OldExportReport(Report):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['supplierName', 'categoryName', 'saleAmount', 'saleIncome',
                                   'totalCost', 'grossProfit', 'grossProfitRate']
        self.SELECTED_COL_IDS = r'C, D, E, F, G, I, J'

    def convertTextDataToDigital(self, df):
        for i in [2]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].transform(self.parseAmount)
        for j in [3, 4, 5]:
            df[self.SELECTED_COL_NAMES[j]] = df[self.SELECTED_COL_NAMES[j]].transform(self.parsePrice)
        return df

    def cleanTableNotSupplier(self, df):
        cleaned_df = DataFrame()
        for i in range(len(df)):
            row = df.loc[i, :]
            # clean empty row
            try:
                if math.isnan(row['supplierName']):
                    continue
            except TypeError:
                if row['supplierName'] not in ['大类名称']:
                    cleaned_df = cleaned_df.append(row)
        return cleaned_df

    def getSupplierName(self, df, ind):
        return df['supplierName'][ind]

    def getCategoryName(self, df, ind):
        return df['categoryName'][ind]

    def getSaleAmount(self, df, ind):
        return df['saleAmount'][ind]

    def getSaleIncome(self, df, ind):
        return round(df['saleIncome'][ind], 2)

    def compareDicts(self, dict_old, dict_new):
        for key in ['saleAmount', 'saleIncome', 'totalCost', 'grossProfit', 'grossProfitRate']:
            if dict_old[key] != dict_new[key]:
                return False
        return True
