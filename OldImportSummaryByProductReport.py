import math

from pandas import DataFrame

from report import Report


class OldImportSummaryByProductReport(Report):

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['serialNum', 'importAmount', 'cost', 'importPrice']
        self.SELECTED_COL_IDS = r'E, G, H, I'
        self.SKIP_ROWS = [0, 1, 2]
        self.COMPARE_COLS = [0, 1, 2]

    def convertTextDataToDigital(self, df):
        for i in [1]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parseAmount)
        for i in [2, 3]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parsePrice)
        return df

    def compareDicts(self, df_old, df_new):
        dict_old = df_old.to_dict('list')
        dict_new = df_new.to_dict('list')
        for key in ['importAmount', 'cost', 'importPrice']:
            try:
                if dict_old[key][0] != dict_new[key][0]:
                    return False
            except IndexError:
                print(dict_old)
                print(dict_new)
                return False
        return True

    def compareArrVals(self, dict_old, dict_new):
        if dict_old.size != dict_new.size:
            return False
        bool_arr = (dict_old.values == dict_new.values)
        for i in self.COMPARE_COLS:
            if not bool_arr[0][i]:
                return False
        return True

    def cleanTable(self, df, col_idx_serial_no):
        cleaned_df = DataFrame()
        for i in range(len(df)):
            row = df.loc[i, :]
            col_name_serial_num = self.SELECTED_COL_NAMES[col_idx_serial_no]
            # clean empty row
            try:
                if math.isnan(row[col_name_serial_num]):
                    continue
            except TypeError:
                if self.isSerialNum(row[col_name_serial_num]):
                    # clean zero price items
                    if row['importAmount'] != "0.00" and row['importPrice'] != "0.00":
                        cleaned_df = cleaned_df.append(row)
        return cleaned_df
