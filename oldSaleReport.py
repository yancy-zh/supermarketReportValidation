#!/usr/bin/python
# -*- coding: UTF-8 -*-
import math
import re

from pandas import DataFrame

from report import Report


class OldSaleReport(Report):
    _SERIAL_PATTERN = r'\d+'
    _ENTRY_NOT_PRODUCT = 0
    _ENTRY_NOT_FOUND = 0

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_IDS = r'E, G, H, I, J, M, N'  # r'D, F, G, H, I, L'
        self.SELECTED_COL_NAMES = ['serialNum', 'saleAmount', 'saleTotal', 'refundAmount', 'refundPrice', 'unit',
                                   'importPrice']

    def getSerialNum(self, df, ind):
        return df['serialNum'][ind]

    def getUnit(self, df, ind):
        return df['unit'][ind]

    def getPrice(self, df, serial_num, colName):
        row_filterd = df[df[self.SELECTED_COL_NAMES[0]] == serial_num]
        value = 0
        try:
            price = row_filterd[colName].iloc[0]
            value = self.parsePrice(price)
        except IndexError:
            print(f"该商品在新系统中不存在 商品编号: {serial_num}")
        return value

    def getAmount(self, df, serial_num, col_name):
        row_filterd = df[df[self.SELECTED_COL_NAMES[0]] == serial_num]
        value = 0
        try:
            price = row_filterd[col_name].iloc[0]
            value = self.parseAmount(price)
        except IndexError:
            print(f"该商品在旧系统中不存在 商品编号: {serial_num}")
            self._ENTRY_NOT_PRODUCT += 1
        return value

    def getSaleAmount(self, df, serial_num):
        return self.getAmount(df, serial_num, self.SELECTED_COL_NAMES[1])

    def getSalePrice(self, df, serial_num):
        return self.getPrice(df, serial_num, self.SELECTED_COL_NAMES[2])

    def getRefundAmount(self, df, serial_num):
        return self.getAmount(df, serial_num, self.SELECTED_COL_NAMES[3])

    def getRefundPrice(self, df, serial_num):
        return self.getPrice(df, serial_num, self.SELECTED_COL_NAMES[4])

    def getNotProductAmount(self):
        return self._ENTRY_NOT_PRODUCT

    def isSerialNum(self, serial_num_str):
        return re.fullmatch(self._SERIAL_PATTERN, serial_num_str)

    def getTotalByCategory(self, df, category):
        row_filterd = df[df[self.SELECTED_COL_NAMES[0]] == category]
        sum_dict = {'sale_amount': 0, 'sale_price': 0, 'refund_amount': 0, 'refund_price': 0}
        try:
            sum_dict['sale_amount'] = self.sumAmount(row_filterd[self.SELECTED_COL_NAMES[1]])
            sum_dict['sale_total'] = round(self.sumPrice(row_filterd[self.SELECTED_COL_NAMES[2]]), 2)
            sum_dict['refund_amount'] = self.sumAmount(row_filterd[self.SELECTED_COL_NAMES[3]])
            sum_dict['refund_price'] = round(self.sumPrice(row_filterd[self.SELECTED_COL_NAMES[4]]), 2)
        except IndexError:
            print(f"该商品在旧系统中不存在 商品编号: {category}")
            self._ENTRY_NOT_FOUND += 1
            return {}
        return sum_dict

    def sumAmount(self, ser):
        sum = 0
        for ind, value in ser.items():
            try:
                sum += self.parseAmount(value)
            except IndexError:
                print(IndexError)
        return sum

    def sumPrice(self, ser):
        sum = 0
        for ind, value in ser.items():
            sum += self.parsePrice(value)
        return sum

    def cleanTable(self, df, col_idx_serial_no):
        cleaned_df = DataFrame()
        for i in range(len(df)):
            row = df.loc[i, :]
            col_name_serial_num = self.SELECTED_COL_NAMES[col_idx_serial_no]
            # clean empty row
            try:
                if math.isnan(row[col_name_serial_num]) is not None:
                    continue
            except TypeError:
                if self.isSerialNum(row[col_name_serial_num]):
                    # clean united sale
                    if len(row[col_name_serial_num]) == 5 or row['importPrice'] == 0 or row['unit'] == "公斤":
                        continue
                    else:
                        cleaned_df = cleaned_df.append(row)
        return cleaned_df
