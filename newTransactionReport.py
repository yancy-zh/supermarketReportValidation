#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from report import Report


class NewTransactionReport(Report):
    _ENTRY_NOT_FOUND = 0
    _SERIAL_PATTERN = r'\d+'

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['itemId', 'saleType', 'productId', 'amount', 'salePrice']
        self.SELECTED_COL_IDS = r'B, G, H, M, Q'

    def isSerialNum(self, serial_num_str):
        return re.fullmatch(self._SERIAL_PATTERN, serial_num_str)

    def calAmountSummary(self, df):
        return df.groupby([self.SELECTED_COL_NAMES[2]])[self.SELECTED_COL_NAMES[3], self.SELECTED_COL_NAMES[4]].sum()

    def convertTextDataToDigital(self, df):
        df[self.SELECTED_COL_NAMES[3]] = df[self.SELECTED_COL_NAMES[3]].map(self.parseAmount)
        df[self.SELECTED_COL_NAMES[4]] = df[self.SELECTED_COL_NAMES[4]].map(self.parsePrice)
        return df
