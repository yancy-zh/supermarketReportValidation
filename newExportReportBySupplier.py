#!/usr/bin/python
# -*- coding: UTF-8 -*-
from newExportReport import NewExportReport


class NewExportReportBySupplier(NewExportReport):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['supplierName', 'serialNum', 'categoryName', 'saleAmount', 'saleIncome',
                                   'totalCost', 'grossProfit', 'grossProfitRate']
        self.SELECTED_COL_IDS = r'D, F, K, M, N, O, Q, R'
