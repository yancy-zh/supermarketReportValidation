from report import Report


class NewImportReport(Report):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['categoryName', 'serialNum', 'avgCost', 'amount', 'importPrice']
        self.SELECTED_COL_IDS = r'F, K, P, S, U'
        self.SKIP_ROWS = [0, 1, 2, 3, 4, 5]

    def convertTextDataToDigital(self, df):
        df['amount'] = df['amount'].map(self.parseAmount)
        for i in [2, 4]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parsePrice)
        return df
