#!/usr/bin/python
# -*- coding: UTF-8 -*-
from report import Report


class NewStockReport(Report):
    # _HEADERS_IMPORT_TEMPLATE_NEW_SYS = ['productId', 'unit', 'amount', 'comment',
    #                                     'productionDate']
    _no_none_data = 0

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['categoryName', 'serialNum', 'productName', 'amount', 'cost',
                                   'currPrice']
        self.SELECTED_COL_IDS = r'C, H, I, L, N, R'  # C, E, F, I, K, O
        self.COMPARE_COLS = [1, 2, 3, 4, 5]

    def getAmount(self, df, productId):
        row_filterd = df[df['serialNum'] == productId]
        new_amount = 0
        try:
            new_amount = row_filterd['amount'].iloc[0]
        except IndexError:
            print(f'该商品在新系统中不存在 商品编号: {productId}')
            self._no_none_data += 1
        return new_amount

    def getPrice(self, df, productId, colName):
        row_filterd = df[df['serialNum'] == productId]
        price = -1
        try:
            price = row_filterd[colName].iloc[0]
        except IndexError:
            print(f"该商品在新系统中不存在 商品编号: {productId}")
        return price

    def getCurrCost(self, df, productId):
        return self.getPrice(df, productId, 'cost')

    def getCurrSalePrice(self, df, productId):
        return self.getPrice(df, productId, 'currPrice')
