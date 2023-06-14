#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import os
import re
from pandas import DataFrame
import math


class OldTransactionRecordReport:
    _SELECTED_COL_NAMES_OLD_SYS = ['saleType', 'itemId', 'productId', 'amount', 'salePrice', 'unit']
    _SELECTED_COL_IDS_OLD_SYS = r'D, E, F, H, J, Q'
    _AMOUNT_PATTERN = re.compile(r'-?\d*\,?\d+\.?\d?\d?')
    _SERIAL_PATTERN = r'\d+'

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

    def getTransactionItem(self, df, ind):
        row = df.iloc[ind]
        row_dict = {}
        row_dict[self._SELECTED_COL_NAMES_OLD_SYS[0]] = row[self._SELECTED_COL_NAMES_OLD_SYS[0]]
        row_dict[self._SELECTED_COL_NAMES_OLD_SYS[1]] = self.parseAmount(row[self._SELECTED_COL_NAMES_OLD_SYS[1]])
        row_dict[self._SELECTED_COL_NAMES_OLD_SYS[2]] = row[self._SELECTED_COL_NAMES_OLD_SYS[2]]
        row_dict[self._SELECTED_COL_NAMES_OLD_SYS[3]] = self.parseAmount(row[self._SELECTED_COL_NAMES_OLD_SYS[3]])
        row_dict[self._SELECTED_COL_NAMES_OLD_SYS[4]] = self.parsePrice(row[self._SELECTED_COL_NAMES_OLD_SYS[4]])
        return row_dict

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
            return float(priceStr)
        else:
            return 0

    def getLineNum(self, df, ind):
        return df[self._SELECTED_COL_NAMES_OLD_SYS[2]][ind]
    def getItemId(self, df, ind):
        return df[self._SELECTED_COL_NAMES_OLD_SYS[1]][ind]
    def isSerialNum(self, serial_num_str):
        return re.fullmatch(self._SERIAL_PATTERN, serial_num_str)

    def cleanTable(self, df):
        cleaned_df = DataFrame()
        for i in range(len(df)):
            row =df.loc[i, :]
            # clean empty row
            try:
                if math.isnan(row[self._SELECTED_COL_NAMES_OLD_SYS[2]]) is not None:
                    continue
            except TypeError:
                if self.isSerialNum(row[self._SELECTED_COL_NAMES_OLD_SYS[2]]):
                    # clean united sale
                    if row[self._SELECTED_COL_NAMES_OLD_SYS[5]] != "公斤" and len(
                            row[self._SELECTED_COL_NAMES_OLD_SYS[2]]) != 5:
                        cleaned_df = cleaned_df.append(row)
        return cleaned_df





