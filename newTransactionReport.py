#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import os
import re
from pandas import DataFrame
import math


class NewTransactionReport:
    _SELECTED_COL_NAMES = ['itemId', 'saleType', 'productId', 'amount', 'salePrice']
    _SELECTED_COL_IDS = r'B, G, H, M, Q'
    _AMOUNT_PATTERN = re.compile(r'-?\d*\,?\d+\.?\d?\d?')
    _ENTRY_NOT_FOUND = 0
    _SERIAL_PATTERN = r'\d+'

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        self.metadata_filename = os.path.join(working_dir_name, reportTableName)
        self.excel_sheet_name = excel_sheet_name

    def importExcelSheet(self):
        if not os.path.isfile(self.metadata_filename):
            print(f"file {self.metadata_filename} doesn't exists")
            return
        df_metadata = pd.read_excel(self.metadata_filename, header=None, skiprows=[0],
                                    usecols=self._SELECTED_COL_IDS,
                                    names=self._SELECTED_COL_NAMES
                                    )
        return df_metadata

    def cleanTable(self, df):
        cleaned_df = DataFrame()
        for i in range(len(df)):
            row = df.loc[i, :]
            # clean empty row
            try:
                if math.isnan(row[self._SELECTED_COL_NAMES[2]]) is not None:
                    continue
            except TypeError:
                if self.isSerialNum(row[self._SELECTED_COL_NAMES[2]]):
                    # clean united sale
                    if len(
                            row[self._SELECTED_COL_NAMES[2]]) != 5:
                        cleaned_df = cleaned_df.append(row)
        return cleaned_df

    def isSerialNum(self, serial_num_str):
        return re.fullmatch(self._SERIAL_PATTERN, serial_num_str)

    def calAmountSummary(self, df):
        return df.groupby([self._SELECTED_COL_NAMES[2]])[self._SELECTED_COL_NAMES[3], self._SELECTED_COL_NAMES[4]].sum()

    def convertTextDataToDigital(self, df):
        df[self._SELECTED_COL_NAMES[3]] = df[self._SELECTED_COL_NAMES[3]].transform(self.parseAmount)
        df[self._SELECTED_COL_NAMES[4]] = df[self._SELECTED_COL_NAMES[4]].transform(self.parsePrice)
        return df

    def parseAmount(self, amountStr):
        try:
            amountStr = amountStr.strip()
        except AttributeError:
            return -1
        amountStr = amountStr.replace(',', '')
        mt = re.match(self._AMOUNT_PATTERN, amountStr)
        if mt:
            return int(float(amountStr))
        else:
            return 0

    def parsePrice(self, priceStr):
        try:
            priceStr = priceStr.strip()
        except AttributeError:
            return -1
        priceStr = priceStr.replace(',', '')
        mt = re.match(self._AMOUNT_PATTERN, priceStr)
        if mt:
            return round(float(priceStr), 2)
        else:
            return 0
