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

    def getSupplierName(self, df):
        return df['supplierName'][0]

    def getAllStatsForGroup(self, groupby_obj, supplier_name, category_name):
        selected_group = groupby_obj.get_group((supplier_name, category_name))
        dict_stats = {}
        dict_stats['saleAmount'] = selected_group['saleAmount'].sum()
        dict_stats['saleIncome'] = round(selected_group['saleIncome'].sum(), 2)
        dict_stats['totalCost'] = round(selected_group['totalCost'].sum(), 2)
        dict_stats['grossProfit'] = round(selected_group['grossProfit'].sum(), 2)
        dict_stats['grossProfitRate'] = round(dict_stats['grossProfit'] / dict_stats['saleIncome'], 4)
        return dict_stats
