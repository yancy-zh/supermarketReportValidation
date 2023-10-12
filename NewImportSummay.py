#!/usr/bin/python
# -*- coding: UTF-8 -*-
from report import Report


class NewImportSummay(Report):
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['serialNum', 'productName', 'amount', 'avgCost', 'importPrice']
        self.SELECTED_COL_IDS = r'C, F, P, Q, S'
        self.SKIP_ROWS = [0, 1, 2, 3, 4, 5]

    def convertTextDataToDigital(self, df):
        df['amount'] = df['amount'].map(self.parseAmount)
        for i in [3, 4]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].map(self.parsePrice)
        return df

    def calAmountSummary(self, df):
        return df.groupby(['serialNum'])

    def getAllStatsForGroup(self, groupby_obj, serial_num):
        selected_group = groupby_obj.get_group(serial_num)
        dict_stats = {}
        dict_stats['amount'] = selected_group['amount'].sum()
        dict_stats['avgCost'] = selected_group['avgCost'].to_list()[0]
        dict_stats['importPrice'] = selected_group['importPrice'].sum()
        return dict_stats

    def compareDicts(self, df_old, df_new):
        dict_old = df_old.to_dict('list')
        dict_new = df_new
        for key in ['amount', 'avgCost', 'importPrice']:
            try:
                if dict_old[key][0] != dict_new[key]:
                    return False
            except IndexError:
                print(dict_old)
                print(dict_new)
                return False
            except KeyError:
                continue
                # print(f"该项无{key}一值。")
        return True
