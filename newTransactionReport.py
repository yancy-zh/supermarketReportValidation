#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import os
import re


class NewTransactionReport:
    _SELECTED_COL_NAMES_OLD_SYS = ['itemId', 'saleType', 'productId', 'amount', 'salePrice']
    _SELECTED_COL_IDS_OLD_SYS = r'B, G, H, M, Q'
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

    def getTranctionItem(self, df, ind):
        pass
