#!/usr/bin/python
# -*- coding: UTF-8 -*-

from report import Report


class OldBasicInfoReport(Report):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_IDS = r'C, D, E, F, G, H, I, J'  # C, D, E, F, G, H, I, K
        self.SELECTED_COL_NAMES = ['categoryName', 'productId', 'serialNum',
                                   'productName', 'unit', 'cost', 'currPrice',
                                   'supplierName']
