#!/usr/bin/python
# -*- coding: UTF-8 -*-
from report import Report


class NewImportSummay(Report):
    # 表13 入库明细汇总
    # 表16 入库单明细汇总
    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['serialNum', 'productName', 'cost', 'importAmount', 'importPrice']
        self.SELECTED_COL_IDS = r'J, L, O, Q, S'
        self.SKIP_ROWS = [0, 1, 2, 3, 4, 5]

    def convertTextDataToDigital(self, df):
        df['importAmount'] = df['importAmount'].map(self.parseAmount)
        for key in ['cost', 'importPrice']:
            df[key] = df[key].map(self.parsePrice)
        return df

    def calAmountSummary(self, df):
        return df.groupby(['serialNum'])

    def getAllStatsForGroup(self, groupby_obj, serial_num):
        selected_group = groupby_obj.get_group(serial_num)
        dict_stats = {}
        dict_stats['importAmount'] = selected_group['importAmount'].sum()
        dict_stats['cost'] = selected_group['cost'].to_list()[0]
        dict_stats['importPrice'] = selected_group['importPrice'].sum()
        return dict_stats

    def compareDicts(self, df_old, df_new):
        dict_old = df_old.to_dict('list')
        dict_new = df_new
        for key in ['importAmount', 'cost', 'importPrice']:
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
