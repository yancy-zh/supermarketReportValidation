#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import os
import re


class OldSaleReport:
    _SELECTED_COL_NAMES_OLD_SYS = ['serialNum', 'saleAmount', 'salePrice', 'refundAmount', 'refundPrice', 'unit']
    _SELECTED_COL_IDS_OLD_SYS = r'D, F, G, H, I, L'
    _AMOUNT_PATTERN = re.compile(r'-?\d*\,?\d+\.?\d?\d?')
    _SERIAL_PATTERN = r'\d+'
    _ENTRY_NOT_PRODUCT = 0
    _ENTRY_NOT_FOUND = 0

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        self.metadata_filename = os.path.join(working_dir_name, reportTableName)
        self.excel_sheet_name = excel_sheet_name

    def importExcelSheet(self):
        if not os.path.isfile(self.metadata_filename):
            print(f"file {self.metadata_filename} doesn't exists")
            return
        df_metadata = pd.read_excel(self.metadata_filename, header=None, skiprows=[0],
                                    usecols=self._SELECTED_COL_IDS_OLD_SYS,
                                    names=self._SELECTED_COL_NAMES_OLD_SYS
                                    )
        return df_metadata

    def getSerialNum(self, df, ind):
        return df['serialNum'][ind]

    def getUnit(self, df, ind):
        return df['unit'][ind]

    def getPrice(self, df, serial_num, colName):
        row_filterd = df[df[self._SELECTED_COL_NAMES_OLD_SYS[0]] == serial_num]
        res = None
        value = 0
        try:
            price = row_filterd[colName].iloc[0]
            [res, value] = self.parsePrice(price)
        except IndexError:
            print(f"该商品在新系统中不存在 商品编号: {serial_num}")
        return [res, value]

    def getAmount(self, df, serial_num, col_name):
        row_filterd = df[df[self._SELECTED_COL_NAMES_OLD_SYS[0]] == serial_num]
        res = None
        value = 0
        try:
            price = row_filterd[col_name].iloc[0]
            [res, value] = self.parseAmount(price)
        except IndexError:
            print(f"该商品在旧系统中不存在 商品编号: {serial_num}")
            self._ENTRY_NOT_PRODUCT += 1
        return [res, value]

    def getSaleAmount(self, df, serial_num):
        return self.getAmount(df, serial_num, self._SELECTED_COL_NAMES_OLD_SYS[1])

    def getSalePrice(self, df, serial_num):
        return self.getPrice(df, serial_num, self._SELECTED_COL_NAMES_OLD_SYS[2])

    def getRefundAmount(self, df, serial_num):
        return self.getAmount(df, serial_num, self._SELECTED_COL_NAMES_OLD_SYS[3])

    def getRefundPrice(self, df, serial_num):
        return self.getPrice(df, serial_num, self._SELECTED_COL_NAMES_OLD_SYS[4])

    def parseAmount(self, amountStr):
        amountStr = amountStr.strip()
        amountStr = amountStr.replace(',', '')
        mt = re.match(self._AMOUNT_PATTERN, amountStr)
        if mt:
            return int(float(amountStr))
        else:
            return 0

    def parsePrice(self, priceStr):
        priceStr = priceStr.strip()
        priceStr = priceStr.replace(',', '')
        mt = re.match(self._AMOUNT_PATTERN, priceStr)
        if mt:
            return float(priceStr)
        else:
            return 0

    def getNotProductAmount(self):
        return self._ENTRY_NOT_PRODUCT

    def isSerialNum(self, serial_num_str):
        return re.fullmatch(self._SERIAL_PATTERN, serial_num_str)

    def getTotalByCategory(self, df, category):
        row_filterd = df[df[self._SELECTED_COL_NAMES_OLD_SYS[0]] == category]
        sum_dict = {'sale_amount': 0, 'sale_price': 0, 'refund_amount': 0, 'refund_price': 0}
        try:
            sum_dict['sale_amount'] = self.sumAmount(row_filterd[self._SELECTED_COL_NAMES_OLD_SYS[1]])
            sum_dict['sale_price'] = self.sumPrice(row_filterd[self._SELECTED_COL_NAMES_OLD_SYS[2]])
            sum_dict['refund_amount'] = self.sumAmount(row_filterd[self._SELECTED_COL_NAMES_OLD_SYS[3]])
            sum_dict['refund_price'] = self.sumPrice(row_filterd[self._SELECTED_COL_NAMES_OLD_SYS[4]])
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
