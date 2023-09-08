#!/usr/bin/python
# -*- coding: UTF-8 -*-

from report import Report


class NewBasicInfoReport(Report):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_IDS = r'A, B, C, I, K, P, W, X'
        self.SELECTED_COL_NAMES = ['productId', 'serialNum', 'productName', 'categoryName',
                                   'supplierName', 'unit', 'currPrice', 'cost'
                                   ]

    def compareDicts(self, dict_old, dict_new):
        if dict_old.size != dict_new.size:
            return False
        bool_arr = (dict_old.values == dict_new.values)
        for i in [1, 2, 3, 4, 5, 6, 7, 8]:
            if not bool_arr[0][i]:
                return False
        return True
