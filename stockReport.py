#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from report import Report

class StockReport(Report):

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_IDS = r'D, F, G, H, I, J, L'
        self.SELECTED_COL_NAMES = ["categoryName", "serialNum", "productName", "unit", "amount", "currCost",
                                       "salePrice"]
    def getProductId(self, df, ind):
        return df['serialNum'][ind]

    def getPrice(self, df, productId, colName):
        row_filterd = df[df[self.SELECTED_COL_NAMES[1]] == productId]
        value = 0
        try:
            price = row_filterd[colName].iloc[0]
            value = self.parsePrice(price)
        except IndexError:
            print(f"该商品在新系统中不存在 商品编号: {productId}")
        return value

    def getCurrCost(self, df, productId):
        return self.getPrice(df, productId, self.SELECTED_COL_NAMES[5])

    def getCurrSalePrice(self, df, productId):
        return self.getPrice(df, productId, self.SELECTED_COL_NAMES[6])

