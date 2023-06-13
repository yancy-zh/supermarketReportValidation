#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
from numpy import NaN
import math
import csv
import os
import xlrd
import string
from productInfo import ProductInfo


class StockReport:
    _SELECTED_COL_NAMES_NEW_SYS = ['productId', 'unit', 'amount', 'comment',
                                   'productionDate']  # '商品编码', "单位", '数量',  '备注','生产日期'
    _SELECTED_COL_IDS_OLD_SYS = r'D, F, G, H, I, J, L'
    _SELECTED_COL_NAMES_OLD_SYS = ["categoryName", "serialNum", "productName", "unit", "amount", "currCost",
                                   "salePrice"]
    _AMOUNT_PATTERN = re.compile(r'-?\d*\,?\d+\.?\d?\d?')

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

    def getProductId(self, df, ind):
        return df['serialNum'][ind]

    def getPrice(self, df, productId, colName):
        row_filterd = df[df[self._SELECTED_COL_NAMES_OLD_SYS[1]] == productId]
        res = None
        value = 0
        try:
            price = row_filterd[colName].iloc[0]
            # TODO:
            [res, value] = self.parsePrice(price)
        except IndexError:
            print(f"该商品在新系统中不存在 商品编号: {productId}")
        return [res, value]

    def getCurrCost(self, df, productId):
        return self.getPrice(df, productId, self._SELECTED_COL_NAMES_OLD_SYS[5])

    def getCurrSalePrice(self, df, productId):
        return self.getPrice(df, productId, self._SELECTED_COL_NAMES_OLD_SYS[6])

    def parseAmount(self, amountStr):
        amountStr = amountStr.strip()
        amountStr = amountStr.replace(',', '')
        mt = re.match(self._AMOUNT_PATTERN, amountStr)
        if mt:
            return [mt, int(float(amountStr))]
        else:
            return [None, -1]

    def parsePrice(self, priceStr):
        priceStr = priceStr.strip()
        priceStr = priceStr.replace(',', '')
        mt = re.match(self._AMOUNT_PATTERN, priceStr)
        if mt:
            return [mt, float(priceStr)]
        else:
            return [None, -1]