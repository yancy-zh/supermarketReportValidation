#!/usr/bin/python
# -*- coding: UTF-8 -*-
from report import Report


class OldImportPurchaseStockGroupBySupplierReport(Report):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['supplierName', 'preSaleAmount', 'preSalePrice', 'importAmount', 'importPrice',
                                   'saleAmount', 'salePrice', 'postSaleAmount', 'postSalePrice']
        self.SELECTED_COL_IDS = r'C, D, E, F, G, H, I, J, K'
        self.CONVERTERS = {}
        self.SKIP_ROWS = []
        self.COMPARE_COLS = [0, 1, 2, 3, 4, 5, 6, 7]
        self.KEY_COL = 'supplierName'
        self.SUPPLIER_NAME_MAP = {'山东鲁花集团商贸有限公司': '山东鲁花集团商贸有限公司西安分公司',
                                  '老牛面粉厂': '陕西老牛面粉有限公司',
                                  '菲达食品公司': '西安菲达食品商贸有限公司',
                                  '蓝鲁蛋糕店': '西安经济技术开发区蓝鲁蛋糕店',
                                  '傲涵贸易有限公司': '西安傲涵贸易有限公司',
                                  '秦南农副产品贸易公司': '西安秦南农副产品贸易有限公司',
                                  '丰泰永泽商贸有限公司': '西安丰泰永泽商贸有限公司',
                                  '腾旺贸易有限公司': '西安腾旺贸易有限公司',
                                  '米脂县李均沟合作社': '米脂县李均沟富产粉条专业合作社',
                                  '小大贸易有限公司': '陕西小大贸易有限公司',
                                  '丹君商贸有限公司': '西安丹君商贸有限公司',
                                  '三炫农业科技': '西安三炫农业科技有限公司',
                                  '西华厨具': '新城区西华陶瓷厨具经营部',
                                  '海和景商贸有限公司': '西安海和景商贸有限公司',
                                  '臻泽农业发展有限公司': '陕西臻泽农业发展有限公司',
                                  '超乐惠有限公司': '西安超乐惠商贸有限公司',
                                  "野森林现代农业公司": '陕西野森林现代农业有限公司',
                                  "品优兴有限公司": '西安品优兴农产品有限公司',
                                  "和天熙商贸有限公司": '西安和天熙商贸有限公司'
                                  }

    def convertTextDataToDigital(self, df):
        for i in [1, 3, 5, 7]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parseAmount)
        for i in [2, 4, 6, 8]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parsePrice)
        return df

    def getSupplierNameNewSys(self, old_name):
        if old_name not in self.SUPPLIER_NAME_MAP.keys():
            return old_name
        return self.SUPPLIER_NAME_MAP.get(old_name)


class NewImportPurchaseStockGroupBySupplierReport(Report):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['supplierName', 'preSaleAmount', 'preSalePrice', 'importAmount', 'importPrice',
                                   'saleAmount', 'salePrice', 'postSaleAmount', 'postSalePrice']
        self.SELECTED_COL_IDS = r'C, G, I, L, N, Q, S, U, V'
        self.CONVERTERS = {}
        self.SKIP_ROWS = {0, 1, 2, 3, 4}
        self.COMPARE_COLS = [0, 1, 2, 3, 4, 5, 6, 7]
        self.KEY_COL = 'supplierName'

    def convertTextDataToDigital(self, df):
        for i in [1, 3, 5, 7]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parseAmount)
        for i in [2, 4, 6, 8]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parsePrice)
        return df
