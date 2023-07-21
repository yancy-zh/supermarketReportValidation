#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from report import Report


class OldTransactionRecordReport(Report):
    _SERIAL_PATTERN = r'\d+'

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['saleType', 'itemId', 'productId', 'amount', 'salePrice', 'unit']
        self.SELECTED_COL_IDS = r'D, E, F, H, J, Q'

    def parseAmount(self, amountStr):
        try:
            amountStr = amountStr.strip()
        except AttributeError:
            return -1
        amountStr = amountStr.replace(',', '')
        mt = re.match(self.AMOUNT_PATTERN, amountStr)
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
        mt = re.match(self.AMOUNT_PATTERN, priceStr)
        if mt:
            return round(float(priceStr), 2)
        else:
            return 0

    def isSerialNum(self, serial_num_str):
        return re.fullmatch(self._SERIAL_PATTERN, serial_num_str)

    def calAmountSummary(self, df):
        return df.groupby([self.SELECTED_COL_NAMES[2]])[self.SELECTED_COL_NAMES[3], self.SELECTED_COL_NAMES[4]].sum()

    def convertTextDataToDigital(self, df):
        df[self.SELECTED_COL_NAMES[3]] = df[self.SELECTED_COL_NAMES[3]].map(self.parseAmount)
        df[self.SELECTED_COL_NAMES[4]] = df[self.SELECTED_COL_NAMES[4]].map(self.parsePrice)
        return df
