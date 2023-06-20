# !/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import os
import re


class NewSaleByCategoryReport:
    _SELECTED_COL_NAMES_OLD_SYS = ['category', 'saleAmount', 'salePrice', 'refundAmount', 'refundPrice']
    _SELECTED_COL_IDS_OLD_SYS = r'D, M, O, P, Q'
    _AMOUNT_PATTERN = re.compile(r'-?\d*\,?\d+\.?\d?\d?')
    _ENTRY_NOT_FOUND = 0

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

    def getTotalByCategory(self, df, category):
        row_filterd = df[df[self._SELECTED_COL_NAMES_OLD_SYS[0]] == category]
        sum_dict = {'sale_amount': 0, 'sale_price': 0, 'refund_amount': 0, 'refund_price': 0}
        try:
            sum_dict['sale_amount'] = self.sumAmount(row_filterd[self._SELECTED_COL_NAMES_OLD_SYS[1]])
            sum_dict['sale_price'] = round(self.sumPrice(row_filterd[self._SELECTED_COL_NAMES_OLD_SYS[2]]), 2)
            sum_dict['refund_amount'] = self.sumAmount(row_filterd[self._SELECTED_COL_NAMES_OLD_SYS[3]])
            sum_dict['refund_price'] = round(self.sumPrice(row_filterd[self._SELECTED_COL_NAMES_OLD_SYS[4]]), 2)
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

    def parseAmount(self, amountStr):
        amountStr = amountStr.strip()
        amountStr = amountStr.replace(',', '')
        mt = re.match(self._AMOUNT_PATTERN, amountStr)
        if mt:
            return int(float(amountStr))
        else:
            return 0

    def parsePrice(self, priceStr):
        priceStr = priceStr.strip()
        priceStr = priceStr.replace(',', '')
        mt = re.match(self._AMOUNT_PATTERN, priceStr)
        if mt:
            return float(priceStr)
        else:
            return 0
