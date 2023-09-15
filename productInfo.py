#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re

import pandas as pd


class ProductInfo:
    _PROUDCT_ID_FORMAT_PATTERN = re.compile("\d{6}")
    _SELECTED_COL_IDS_PRODUCT_INFO_OLD_SYS = r'D, G, H, I, K'
    _SELECTED_COL_NAMES_PRODUCT_INFO_OLD_SYS = ['productId', 'unit', 'currCost', 'salePrice',
                                                'supplierName']  # '货号', '单位','当前进价','当前售价','供货商名称'
    _AMOUNT_PATTERN = re.compile(r'-?\d*\,?\d+\.?\d?\d?')
    _SERIAL_NUM_PATTERN = re.compile(r'\d+')
    def __init__(self, working_dir_name, base_info_table_name, excel_sheet_name):
        self.working_dir_name = working_dir_name
        self.base_info_table_name = base_info_table_name
        self.product_info_filename = os.path.join(working_dir_name, self.base_info_table_name)
        self.excel_sheet_name = excel_sheet_name
        self.excel_selected_column_ids = self._SELECTED_COL_IDS_PRODUCT_INFO_OLD_SYS
        self.excel_selected_column_names = self._SELECTED_COL_NAMES_PRODUCT_INFO_OLD_SYS

    def importProductMetaData(self):
        if not os.path.isfile(self.product_info_filename):
            print(f"file {self.product_info_filename} doesn't exists")
        return pd.read_excel(self.product_info_filename, header=None, skiprows=[0],
                             usecols=self.excel_selected_column_ids,
                             names=self.excel_selected_column_names
                             )

    def getProductIdLs(self, df):
        productid_col = df[self._SELECTED_COL_NAMES_PRODUCT_INFO_OLD_SYS[0]]
        id_ls = []
        for it in productid_col:
            mt = re.match(self._PROUDCT_ID_FORMAT_PATTERN, it)
            if not mt:
                continue
            else:
                id_ls.append(id)
                # TODO
        return id_ls

    def cvtProductIdFormat(self, idStr):
        mt = re.match(self._PROUDCT_ID_FORMAT_PATTERN, idStr)
        return mt

    def parseAmount(self, amountStr):
        amountStr = amountStr.strip()
        amountStr = amountStr.replace(',', '')
        mt = re.match(self._AMOUNT_PATTERN, amountStr)
        if mt:
            return [mt, int(float(amountStr))]
        else:
            return [None, -1]
