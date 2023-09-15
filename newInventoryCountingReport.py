#!/usr/bin/python
# -*- coding: UTF-8 -*-
from report import Report


class NewInventoryCountingReport(Report):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['serialNum', 'stockAmount', 'countingAmount', 'diffAmount', 'diffPrice']
        self.SELECTED_COL_IDS = r'D,H,L,M,O'
        self.COMPARE_COLS = [1, 2, 3, 4]

    def convertTextDataToDigital(self, df):
        df[self.SELECTED_COL_NAMES[4]] = df[self.SELECTED_COL_NAMES[1]].map(self.parsePrice)
        for i in [1, 2, 3]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parseAmount)
        return df
