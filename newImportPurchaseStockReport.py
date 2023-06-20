from report import Report


class NewImportPurchaseStockReport(Report):

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['serialNum', 'preSaleCost', 'preSaleAmount', 'preSalePrice', 'importAmount',
                                   'importPrice', 'saleAmount', 'salePrice', 'postSaleAmount', 'postSalePrice']
        self.SELECTED_COL_IDS = r'D, J, M, P, Q, R, S, T, V, W'

    def convertTextDataToDigital(self, df):
        for i in [2, 4, 6, 8]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].transform(self.floatToInt)
        for j in [1, 3, 5, 7, 9]:
            df[self.SELECTED_COL_NAMES[j]] = df[self.SELECTED_COL_NAMES[j]].transform(self.roundPrice)
        return df

    def removeKeyFromDict(self, dict):
        try:
            del dict['_0']
        except TypeError:
            print(f'dict doesn\'t contain _0')
        except KeyError:
            print(f'dict doesn\'t contain _0')
        try:
            del dict['Unnamed: 0']
            return dict
        except TypeError:
            print(f'dict doesn\'t contain Unnamed: 0')
        except KeyError:
            print(f'dict doesn\'t contain Unnamed: 0')
        return dict
