from report import Report


class OldImportReport(Report):

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['serialNum', 'amount', 'avgCost', 'importPrice']
        self.SELECTED_COL_IDS = r'C, E, F, G'
        self.SKIP_ROWS = [0, 1, 2]

    def convertTextDataToDigital(self, df):
        df[self.SELECTED_COL_NAMES[1]] = df[self.SELECTED_COL_NAMES[1]].map(self.parseAmount)
        for i in [2, 3]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parsePrice)
        return df

    def compareDicts(self, df_old, df_new):
        dict_old = df_old.to_dict('list')
        dict_new = df_new.to_dict('list')
        for key in ['amount', 'avgCost', 'importPrice']:
            try:
                if dict_old[key][0] != dict_new[key][0]:
                    return False
            except IndexError:
                print(dict_old)
                print(dict_new)
                return False
        return True
