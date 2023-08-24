#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

import pandas as pd

from report import Report


class NewSaleReport(Report):
    _ENTRY_NOT_PRODUCT = 0
    _ENTRY_NOT_FOUND = 0
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_IDS = r'F, K, L, N, O, Q' #'E, J, K, L, M, O'
        self.SELECTED_COL_NAMES = ['serialNum', 'saleAmount', 'salePrice', 'refundAmount', 'refundPrice', 'importPrice']
    def importExcelSheet(self):
        if not os.path.isfile(self.metadata_filename):
            print(f"file {self.metadata_filename} doesn't exists")
            return
        df_metadata = pd.read_excel(self.metadata_filename, header=None, skiprows=[0],
                                    usecols=self.SELECTED_COL_IDS,
                                    names=self.SELECTED_COL_NAMES
                                    )
        return df_metadata

    def getSerialNum(self, df, ind):
        return df['serialNum'][ind]

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
            print(f"该商品在新系统中不存在 商品编号: {serial_num}")
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

