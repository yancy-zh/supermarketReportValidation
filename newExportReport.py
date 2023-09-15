#!/usr/bin/python
# -*- coding: UTF-8 -*-
from report import Report


class NewExportReport(Report):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['supplierName', 'serialNum', 'categoryName', 'saleAmount', 'saleIncome',
                                   'totalCost', 'grossProfit', 'grossProfitRate']
        self.SELECTED_COL_IDS = r'D, G, L, N, O, P, R, S'

    def getPrice(self, df, serial_num, colName):
        row_filterd = df[df[self.SELECTED_COL_NAMES[1]] == serial_num]
        value = 0
        try:
            price = row_filterd[colName].iloc[1]
            value = self.parsePrice(price)
        except IndexError:
            print(f"该商品在新系统中不存在 商品编号: {serial_num}")
        return value

    def getSalePrice(self, df, serial_num):
        return self.getPrice(df, serial_num, self.SELECTED_COL_NAMES[4])

    def getTotalCost(self, df, serial_num):
        return self.getPrice(df, serial_num, self.SELECTED_COL_NAMES[6])

    def getGrossProfit(self, df, serial_num):
        return self.getPrice(df, serial_num, self.SELECTED_COL_NAMES[6])

    def calAmountSummary(self, df):
        return df.groupby(['supplierName', 'categoryName'])
