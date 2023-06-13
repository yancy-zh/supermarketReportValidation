#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import os
import re


class NewStockReport:
    _HEADERS_IMPORT_TEMPLATE_NEW_SYS = ['productId', 'unit', 'amount', 'comment',
                                        'productionDate']

    _SELECTED_COL_NAMES_STOCK_REPORT_NEW_SYS = ['categoryName', 'productName', 'serialNum', 'amount', 'cost',
                                                'currPrice']
    _SELECTED_COL_IDS_STOCK_REPORT_NEW_SYS = r'C, E, G, I, K, O'
    _SHEET_NAME = "Sheet1"
    _no_none_data = 0
    _AMOUNT_PATTERN = re.compile(r'-?\d*\,?\d+\.?\d?\d?')

    def __init__(self, working_dir_name, reportTableName):
        self.metadata_filename = os.path.join(working_dir_name, reportTableName)

    def importExcelSheet(self):
        if not os.path.isfile(self.metadata_filename):
            print(f"file {self.metadata_filename} doesn't exists")
            return
        dict_metadata = pd.read_excel(self.metadata_filename, header=None, skiprows=[0],
                                      usecols=self._SELECTED_COL_IDS_STOCK_REPORT_NEW_SYS,
                                      names=self._SELECTED_COL_NAMES_STOCK_REPORT_NEW_SYS,
                                      sheet_name=self._SHEET_NAME
                                      )
        return dict_metadata

    def getAmount(self, df, productId):
        row_filterd = df[df[self._SELECTED_COL_NAMES_STOCK_REPORT_NEW_SYS[2]] == productId]
        new_amount = 0
        try:
            new_amount = row_filterd['amount'].iloc[0]
        except IndexError:
            # print(f'该商品在新系统中不存在 商品编号: {productId}')
            self._no_none_data += 1
        return new_amount

    def getPrice(self, df, productId, colName):
        row_filterd = df[df[self._SELECTED_COL_NAMES_STOCK_REPORT_NEW_SYS[2]] == productId]
        price = -1
        try:
            price = row_filterd[colName].iloc[0]
        except IndexError:
            print(f"该商品在新系统中不存在 商品编号: {productId}")
        return price

    def getCurrCost(self, df, productId):
        return self.getPrice(df, productId, self._SELECTED_COL_NAMES_STOCK_REPORT_NEW_SYS[4])

    def getCurrSalePrice(self, df, productId):
        return self.getPrice(df, productId, self._SELECTED_COL_NAMES_STOCK_REPORT_NEW_SYS[5])

    def parseAmount(self, amountStr):
        if isinstance(amountStr, int):
            return amountStr
        mt = re.match(self._AMOUNT_PATTERN, amountStr)
        if mt:
            return int(float(amountStr))
        else:
            return -1
