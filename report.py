#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import os
import re
from pandas import DataFrame
import math


class Report:
    SELECTED_COL_NAMES = []
    SELECTED_COL_IDS = ''
    AMOUNT_PATTERN = re.compile(r'-?\d*\,?\d+\.?\d?\d?')
    SERIAL_PATTERN = r'\d+'
    CONVERTERS = {'serialNum': str}

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        self.metadata_filename = os.path.join(working_dir_name, reportTableName)
        self.excel_sheet_name = excel_sheet_name

    def importExcelSheet(self):
        if not os.path.isfile(self.metadata_filename):
            print(f"file {self.metadata_filename} doesn't exists")
            return
        df_metadata = pd.read_excel(self.metadata_filename, header=None, skiprows=[0],
                                    usecols=self.SELECTED_COL_IDS,
                                    names=self.SELECTED_COL_NAMES,
                                    converters=self.CONVERTERS
                                    )
        return df_metadata

    def isSerialNum(self, serial_num_str):
        return re.fullmatch(self.SERIAL_PATTERN, serial_num_str)

    def parseAmount(self, amountStr):
        amountStr = amountStr.replace(',', '')
        try:
            mt = re.match(self.AMOUNT_PATTERN, amountStr)
        except TypeError:
            print(TypeError)
            mt = None
        if mt:
            return int(float(amountStr))
        else:
            return -1000

    def floatToInt(self, num_float):
        return int(num_float)

    def roundPrice(self, price):
        return round(price, 2)

    def parsePrice(self, priceStr):
        try:
            priceStr = priceStr.strip()
        except AttributeError:
            return -1
        priceStr = priceStr.replace(',', '')
        mt = re.match(self.AMOUNT_PATTERN, priceStr)
        if mt:
            return round(float(priceStr), 2)
        else:
            return 0.00

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
                    if len(
                            row[col_name_serial_num]) != 5:
                        cleaned_df = cleaned_df.append(row)
        return cleaned_df

    def getRowByInd(self, df, ind):
        return df.iloc[ind]

    def seriesToDict(self, ser):
        return ser.to_dict()

    def dfToDict(self, df):
        try:
            dict = df.to_dict(orient='records')[0]
        except IndexError:
            serial_no = df['serialNum']
            print(f'{serial_no} format not right')
            dict = df.to_dict()
        return dict

    def getRowBySerialNum(self, df, serial_num):
        return df[df['serialNum'] == serial_num]

    def compareDicts(self, dict_old, dict_new):
        if dict_old.size != dict_new.size:
            return False
        bool_arr = (dict_old.values == dict_new.values)
        for i in [1, 2, 3, 4, 5, 7, 8, 9]:
            if not bool_arr[0][i]:
                return False
        return True
