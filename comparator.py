#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd


class Comparator:
    def __init__(self, old_report, new_report, program_name, date_time):
        self.old_report = old_report
        self.new_report = new_report
        self.program_name = program_name
        self.date_time = date_time

    def printLogHeaderOldAndNew(self):
        print(
            f"运行{self.program_name}，文件名：\n-{self.old_report}\n-{self.new_report}\n日期：{self.date_time}...")

    def saveToCsvs(self, df_old, df_new, csv_prefix):
        df_old.to_csv(f'{csv_prefix}_df_old_sys.csv')
        df_new.to_csv(f'{csv_prefix}_df_new_sys.csv')

    def loadCsvsToDataframe(self, csv_prefix):
        df_old = pd.read_csv(f'{csv_prefix}_df_old_sys.csv')
        df_new = pd.read_csv(f'{csv_prefix}_df_new_sys.csv')
        return [df_old, df_new]

    def printItemUnequalResult(self, serial_num, old_dict, new_dict):
        print(f'商品：{serial_num}数据对不上:\n - 旧系统：{old_dict}\n- 新系统：{new_dict}')

    def printTotalResult(self, total, no_correct, no_incorrect):
        print(f'总数据行数：{total}')
        print(f'数据正确共：{no_correct}\n数据错误共：{no_incorrect}')

    def printSeparationLine(self):
        print(u'\u2015' * 10)

    def printNewSysNotFound(self, item_name):
        print(item_name + "在新系统中不存在。")
