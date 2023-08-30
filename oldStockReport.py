#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from report import Report
from pandas import DataFrame
import math


class OldStockReport(Report):

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
                # check if serial num is in the right format,
                # serial num isn't a united item,
                # stock amount is not zero.
                if self.isSerialNum(row[col_name_serial_num]) is not None and \
                        len(row[col_name_serial_num]) != 5 and \
                        self.parseAmount(row['amount']) != 0:
                    cleaned_df = cleaned_df.append(row)
        return cleaned_df
