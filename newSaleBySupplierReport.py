#!/usr/bin/python
# -*- coding: UTF-8 -*-
from report import Report


class NewSaleBySupplierReport(Report):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['supplierName', 'saleAmount', 'salePrice', 'refundAmount', 'refundPrice',
                                   'actualAmount',
                                   'actualPrice']
        self.SELECTED_COL_IDS = r'D, J, K, L, O, S, U'
        self.CONVERTERS = {}
        self.SKIP_ROWS = []
        self.COMPARE_COLS = [0, 1, 2, 3, 4, 5]
        self.KEY_COL = 'supplierName'

    def convertTextDataToDigital(self, df):
        for i in [1, 3, 5]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parseAmount)
        for i in [2, 4, 6]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parsePrice)
        return df
