from report import Report


class OldImportPurchaseStockReport(Report):

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['serialNum', 'preSaleAmount', 'preSalePrice', 'importAmount', 'preSaleCost',
                                   'postSaleAmount', 'postSalePrice', 'importPrice', 'saleAmount', 'salePrice']
        self.SELECTED_COL_IDS = r'C, E, F, H, I, J, M, P, AG, AI'


    def convertTextDataToDigital(self, df):
        df[self.SELECTED_COL_NAMES[3]] = df[self.SELECTED_COL_NAMES[3]].transform(self.floatToInt)
        df[self.SELECTED_COL_NAMES[8]] = df[self.SELECTED_COL_NAMES[8]].transform(self.floatToInt)
        df[self.SELECTED_COL_NAMES[5]] = df[self.SELECTED_COL_NAMES[5]].transform(self.parseAmount)
        df[self.SELECTED_COL_NAMES[1]] = df[self.SELECTED_COL_NAMES[1]].transform(self.parseAmount)
        for i in [2, 4, 6, 7, 9]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].transform(self.roundPrice)
        return df

    def removeKeyFromDict(self, dict):
        try:
            del dict['Unnamed: 0']
            return dict
        except TypeError:
            print(f'dict doesn\'t contain Unnamed: 0')
