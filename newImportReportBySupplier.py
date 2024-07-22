#!/usr/bin/python
# -*- coding: UTF-8 -*-
from report import Report


class NewImportReportBySupplier(Report):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['supplierName', 'importAmount', 'importPrice']
        self.SELECTED_COL_IDS = r'D, N, R'
        self.KEY_COL = 'supplierName'

    def convertTextDataToDigital(self, df):
        for i in [1]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].transform(self.parseAmount)
        for j in [2]:
            df[self.SELECTED_COL_NAMES[j]] = df[self.SELECTED_COL_NAMES[j]].transform(self.parsePrice)
        return df
