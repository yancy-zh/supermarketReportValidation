# !/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import os
import re
from report import Report

class NewSaleByCategoryReport(Report):
    _ENTRY_NOT_FOUND = 0

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['category', 'saleAmount', 'salePrice', 'refundAmount', 'refundPrice']
        self.SELECTED_COL_IDS = r'D, M, O, P, Q'

    def getTotalByCategory(self, df, category):
        row_filterd = df[df[self.SELECTED_COL_NAMES[0]] == category]
        sum_dict = {'sale_amount': 0, 'sale_price': 0, 'refund_amount': 0, 'refund_price': 0}
        try:
            sum_dict['sale_amount'] = self.sumAmount(row_filterd[self.SELECTED_COL_NAMES[1]])
            sum_dict['sale_price'] = round(self.sumPrice(row_filterd[self.SELECTED_COL_NAMES[2]]), 2)
            sum_dict['refund_amount'] = self.sumAmount(row_filterd[self.SELECTED_COL_NAMES[3]])
            sum_dict['refund_price'] = round(self.sumPrice(row_filterd[self.SELECTED_COL_NAMES[4]]), 2)
        except IndexError:
            print(f"该商品在新系统中不存在 商品编号: {category}")
            self._ENTRY_NOT_FOUND += 1
            return {}
        return sum_dict

    def sumAmount(self, ser):
        sum = 0
        for ind, value in ser.items():
            try:
                sum += self.parseAmount(value)
            except IndexError:
                print(IndexError)
        return sum

    def sumPrice(self, ser):
        sum = 0
        for ind, value in ser.items():
            sum += self.parsePrice(value)
        return sum
