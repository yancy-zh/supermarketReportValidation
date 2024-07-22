from report import Report


class NewImportInvoiceReport(Report):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['serialNum', 'amount', 'avgCost', 'importPrice']
        self.SELECTED_COL_IDS = r'C, W, X, AA'
        self.SKIP_ROWS = [0, 1, 2, 3, 4]

    def convertTextDataToDigital(self, df):
        for i in [1]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parseAmount)
        for i in [2, 3]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parsePrice)
        return df
