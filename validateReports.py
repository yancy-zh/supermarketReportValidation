#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime

import pandas as pd

from newImportPurchaseStockReport import NewImportPurchaseStockReport
from stockReport import StockReport
from newStockReport import NewStockReport
from oldSaleReport import OldSaleReport
from newSaleReport import NewSaleReport
from oldTransactionRecordReport import OldTransactionRecordReport
from newSaleByCategoryReport import NewSaleByCategoryReport
from newTransactionReport import NewTransactionReport
from pandas import DataFrame
import math
from oldImportPurchaseStockReport import OldImportPurchaseStockReport


class ValidateReports:
    _STOCK_VALIDATION_WORKING_DIR_OLD_SYS = r"D:\微云同步助手\89151701\liangli\proj\data\old\20230606"
    _STOCK_VALIDATION_WORKING_DIR_NEW_SYS = r"D:\微云同步助手\89151701\liangli\proj\data\new\20230606"
    _DATETIME_TO_VALIDATE = datetime.datetime(year=2023, month=6, day=6)
    _FORMAT_OF_PRINTED_DATE = "%Y-%m-%d"
    _SHEET_NAME = "Sheet1"

    def __init__(self):
        pass

    def validateStockReports(self, name):
        # compare two stock reports
        # parameters
        OLD_STOCK_REPORT_FILENAME = r"6.5库存.xls"
        NEW_STOCK_REPORT_FILENAME = r"3 商品库存汇总报表.xls"

        print(
            f'Hi, {name} for date {self._DATETIME_TO_VALIDATE.__format__(self._FORMAT_OF_PRINTED_DATE)}')  # Press Ctrl+Shift+B to toggle the breakpoint.
        # import excel sheets
        old_stock_report = StockReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_STOCK_REPORT_FILENAME,
                                       self._SHEET_NAME)
        df_stock_old_sys = old_stock_report.importExcelSheet()
        new_stock_report = NewStockReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_STOCK_REPORT_FILENAME)
        df_stock_new_sys = new_stock_report.importExcelSheet()
        total_line_num = df_stock_old_sys.index.size
        no_zero_amount = 0
        no_none_data = 0
        no_subtotal = 0
        no_naf = 0
        no_amount_correct = 0
        no_cost_correct = 0
        no_cost_incorrect = 0
        no_sale_price_correct = 0
        no_sale_price_incorrect = 0
        # compare amount
        for ind in df_stock_old_sys.index:
            old_amount_str = df_stock_old_sys['amount'][ind]
            if old_amount_str is None:
                no_none_data += 1
                continue
            try:
                [res, old_amount] = old_stock_report.parseAmount(old_amount_str)
                if res is None:
                    no_naf += 1
                    continue
                elif old_amount == 0:
                    no_zero_amount += 1
                    continue
            except TypeError:
                print("旧系统表中该行包含错误数据")
                continue
            tmp_productId = old_stock_report.getProductId(df_stock_old_sys, ind)
            # check amount
            new_amount = new_stock_report.getAmount(df_stock_new_sys, tmp_productId)
            if old_amount == new_amount:
                no_amount_correct += 1
            else:
                print(f"商品 {tmp_productId} 的数量核对不上，在旧系统中为：{old_amount}，在新系统中为{new_amount}")
            # check currCost
            [res, old_cost] = old_stock_report.getCurrCost(df_stock_old_sys, tmp_productId)
            if res is None:
                print("该行没有数据")
                continue
            new_cost = new_stock_report.getCurrCost(df_stock_new_sys, tmp_productId)
            if old_cost == new_cost:
                no_cost_correct += 1
            elif old_cost != new_cost:
                no_cost_incorrect += 1
                print(f"商品 {tmp_productId} 的成本价核对不上，在旧系统中为：{old_cost}，在新系统中为{new_cost}")
            # check salePrice
            [res, old_sale_price] = old_stock_report.getCurrSalePrice(df_stock_old_sys, tmp_productId)
            if res is None:
                print("this line doesn't contain data")
                continue
            new_salePrice = new_stock_report.getCurrSalePrice(df_stock_new_sys, tmp_productId)
            if old_sale_price == new_salePrice:
                no_sale_price_correct += 1
            elif old_sale_price != new_salePrice:
                no_sale_price_incorrect += 1
                print(f"商品 {tmp_productId} 的成本价核对不上，在旧系统中为：{old_cost}，在新系统中为{new_salePrice}")
        print(
            f'{name} ended...\n总处理行数: {total_line_num} 个\n数量正确: {no_amount_correct} 个\n数量为零: {no_zero_amount}\n数量非浮点数: {no_naf}\n无数据: {no_none_data} 个\n')
        print(f'成本价正确: {no_cost_correct} 个\n成本价错误: {no_cost_incorrect} 个\n')
        print(f'销售价正确: {no_sale_price_correct} 个\n销售价错误: {no_sale_price_incorrect} 个\n')

    def validatePurchaseSaleStockReports(self, name):
        print(f'运行：{name}')
        OLD_REPORT_FILENAME = r"6.6动态明细.xls"
        NEW_REPORT_FILENAME = r"4 商品进销存汇总表.xls"
        no_correct = 0
        no_incorrect = 0
        # initialize objs
        report_old = OldImportPurchaseStockReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                                  self._SHEET_NAME)
        report_new = NewImportPurchaseStockReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME,
                                                  self._SHEET_NAME)
        # import excel sheets
        # df_old = report_old.importExcelSheet()
        # df_new = report_new.importExcelSheet()
        # # clean up the table
        # df_old = report_old.cleanTable(df_old, 0)
        # df_new = report_new.cleanTable(df_new, 0)
        # # write data to csv
        # df_old.to_csv(f'{name}old_report_cleaned.csv')
        # df_new.to_csv(f'{name}new_report_cleaned.csv')

        # import csv to df
        df_old = pd.read_csv("比对进销存表old_report_cleaned.csv")
        df_new = pd.read_csv("比对进销存表new_report_cleaned.csv")
        # convert text data to digital
        df_old = report_old.convertTextDataToDigital(df_old)
        df_new = report_new.convertTextDataToDigital(df_new)
        # loop in the table
        for ind in df_old.index:
            serial_num = df_old['serialNum'][ind]
            old_dict = report_old.getRowBySerialNum(df_old, serial_num)
            new_dict = report_new.getRowBySerialNum(df_new,  serial_num)
            # old_dict = report_old.removeKeyFromDict(old_dict)
            # new_dict = report_new.removeKeyFromDict(new_dict)
            if report_old.compareDicts(old_dict, new_dict):
                no_correct += 1
            else:
                no_incorrect += 1
                print(f'商品：{serial_num}数据对不上:\n - 旧系统：{old_dict}\n- 新系统：{new_dict}')
        print(f'总数据行数：{len(df_old)}')
        print(f'数据正确共：{no_correct}\n数据错误共：{no_incorrect}')

    def validateSaleReports(self, name):
        print(f"运行{name}...")
        OLD_REPORT_FILENAME = r"6.6销售表.xls"
        NEW_REPORT_FILENAME = r"7 便利一店销售汇总报表（品名排序）.xls"
        # import excel sheets
        old_report = OldSaleReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                   self._SHEET_NAME)
        df_old_sys = old_report.importExcelSheet()
        new_report = NewSaleReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME, self._SHEET_NAME)
        df_new_sys = new_report.importExcelSheet()
        total_line_num = df_old_sys.index.size
        no_product = 0
        no_none_data = 0
        no_sub_total = 0
        no_naf = 0
        no_sale_amount_correct = 0
        no_sale_amount_incorrect = 0
        no_united_sale = 0
        no_sale_price_correct = 0
        no_sale_price_incorrect = 0
        no_refund_amount_correct = 0
        no_refund_amount_incorrect = 0
        no_refund_price_correct = 0
        no_refund_price_incorrect = 0
        for ind in df_old_sys.index:
            # skip the product which unit is jin
            if old_report.getUnit(df_old_sys, ind) == "公斤":
                no_united_sale += 1
                continue
            serial_num = old_report.getSerialNum(df_old_sys, ind)
            try:
                if math.isnan(serial_num):
                    continue
            except TypeError:
                no_none_data += 1
                if old_report.isSerialNum(serial_num) is None:
                    no_sub_total += 1
                    continue
            if len(serial_num) < 6:
                no_united_sale += 1
                continue
            # compare sale amount
            old_sale_amount = 0
            try:
                [res, old_sale_amount] = old_report.getSaleAmount(df_old_sys, serial_num)
                if res is None:
                    no_naf += 1
                    print("数量格式有误")
            except TypeError:
                print("旧系统表中该行包含错误数据")
                continue
            [res, new_sale_amount] = new_report.getSaleAmount(df_new_sys, serial_num)
            if new_sale_amount == old_sale_amount:
                no_product += 1
                no_sale_amount_correct += 1
            else:
                no_product += 1
                no_sale_amount_incorrect += 1
                print(
                    f"商品 {serial_num} 的銷售数量核对不上，在旧系统中为：{old_sale_amount}，在新系统中为{new_sale_amount}")
            # compare refund amount
            try:
                [res, old_refund_amount] = old_report.getRefundAmount(df_old_sys, serial_num)
                if res is None:
                    no_naf += 1
                    print("数量格式有误")
            except TypeError:
                print("旧系统表中该行包含错误数据")
                continue
            [res, new_refund_amount] = new_report.getRefundAmount(df_new_sys, serial_num)
            if new_refund_amount == old_refund_amount:
                no_refund_amount_correct += 1
            else:
                no_refund_amount_incorrect += 1
                print(
                    f"商品 {serial_num} 的退貨数量核对不上，在旧系统中为：{old_refund_amount}，在新系统中为{new_refund_amount}")
            # compare sale price
            [_, old_sale_price] = old_report.getSalePrice(df_old_sys, serial_num)
            [_, new_sale_price] = new_report.getSalePrice(df_new_sys, serial_num)
            if old_sale_price == new_sale_price:
                no_sale_price_correct += 1
            else:
                no_sale_price_incorrect += 1
                print(
                    f"商品 {serial_num} 的销售金额核对不上，在旧系统中为：{old_sale_price}，在新系统中为{new_sale_price}")
            # compare refund price
            [_, old_refund_price] = old_report.getRefundPrice(df_old_sys, serial_num)
            [_, new_refund_price] = new_report.getRefundPrice(df_new_sys, serial_num)
            if old_refund_price == new_refund_price:
                no_refund_price_correct += 1
            else:
                no_refund_price_incorrect += 1
                print(
                    f"商品 {serial_num} 的退貨金额核对不上，在旧系统中为：{old_refund_price}，在新系统中为{new_refund_price}")
        print(
            f'总行数：{total_line_num}\n无数据：{no_none_data}\n小计行数:{no_sub_total}\n发生变动的总商品数量为：{no_product}\n联营商品数量：{no_united_sale}\n销售数量正确的商品个数：{no_sale_amount_correct}\n销售数量错误的商品个数：{no_sale_amount_incorrect}')
        print(f'商品销售金额正确：{no_sale_price_correct}\n商品销售金额错误：{no_sale_price_incorrect}')
        print(f'商品退货数量正确：{no_refund_amount_correct}\n商品退货数量错误：{no_refund_amount_incorrect}')
        print(f'商品退货金额正确：{no_refund_price_correct}\n商品退货金额错误：{no_refund_price_incorrect}')

    def validateSaleByCategory(self, name):
        OLD_REPORT_FILENAME = r"6.6销售表.xls"
        NEW_REPORT_FILENAME = r"7 便利一店销售汇总报表（品类排序）.xls"
        no_category_sum_correct = 0
        no_category_sum_incorrect = 0
        # import excel sheets
        old_report = OldSaleReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                   self._SHEET_NAME)
        df_old_sys = old_report.importExcelSheet()
        new_report = NewSaleByCategoryReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME,
                                             self._SHEET_NAME)
        df_new_sys = new_report.importExcelSheet()
        ls = ["食用油", "调料", "副食", "大米", "面粉", "零食", "饮料", "副食", "乳制品", "蔬菜", "水果"
            , "鸡蛋", "乳制品酸奶", "乳制品纯奶", "杂品类（购物袋）", "调料"
            , "干货", "杂粮", "肉类", "冻货", "蛋糕"]
        categories = set(ls)
        for category in categories:
            old_sum_dict = old_report.getTotalByCategory(df_old_sys, category)
            new_sum_dict = new_report.getTotalByCategory(df_new_sys, category)
            if old_sum_dict == new_sum_dict:
                no_category_sum_correct += 1
            else:
                no_category_sum_incorrect += 1
                print(f'品类{category}数据对不上:\n - 旧系统：{old_sum_dict}\n- 新系统：{new_sum_dict}')
        print(f"品类数量共：{len(categories)}\n分别是：{categories}")
        print(f'数据正确共：{no_category_sum_correct}\n数据错误共：{no_category_sum_incorrect}')

    def validateTransactionReports(self, name):
        print(f"运行{name}...")
        OLD_REPORT_FILENAME = r"6.6前台流水.xls"
        NEW_REPORT_FILENAME = r"9 前台商品销售流水.xls"

        # import excel sheets
        old_report = OldTransactionRecordReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                                self._SHEET_NAME)
        df_old_sys = old_report.importExcelSheet()
        new_report = NewTransactionReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME,
                                          self._SHEET_NAME)
        df_new_sys = new_report.importExcelSheet()
        df_old_sys_cleaned = old_report.cleanTable(df_old_sys)
        df_old_sys_amount_sum = old_report.calAmountSummary(old_report.convertTextDataToDigital(df_old_sys_cleaned))
        df_old_sys_amount_sum.to_csv(f'{name}df_old_sys_amount_sum.csv')
        df_new_sys_cleaned = new_report.cleanTable(df_new_sys)
        df_new_sys_amount_sum = new_report.calAmountSummary(new_report.convertTextDataToDigital(df_new_sys_cleaned))
        df_new_sys_amount_sum.to_csv(f'{name}df_new_sys_amount_sum.csv')

    def compareTransactionReports(self, name):
        print(f'运行：{name}')
        df_old = pd.read_csv("比对流水表df_old_sys_amount_sum.csv")
        df_new = pd.read_csv("比对流水表df_new_sys_amount_sum.csv")
        total = len(df_old.index)
        no_correct = 0
        no_incorrect = 0
        no_index_err = 0
        no_val_err = 0
        for ind in df_old.index:
            productId = df_old['productId'][ind]
            row_in_new_sys = df_new[df_new['productId'] == productId]
            old_amount = df_old['amount'][ind]
            old_price = df_old['salePrice'][ind]
            try:
                new_amount = row_in_new_sys.get('amount').values[0]
                new_price = row_in_new_sys.get('salePrice').values[0]
            except IndexError:
                no_index_err += 1
                new_amount = row_in_new_sys.get('amount')
                new_price = row_in_new_sys.get('salePrice')
                print(
                    f'{IndexError}ind: {ind}商品货号：{productId}数据比对不上\n旧系统销售数量：{old_amount} 销售金额: {old_price}')
                print(f'新系统销售数量：{new_amount} 销售金额: {new_price}')
            try:
                if old_amount == new_amount and round(old_price, 2) == round(new_price, 2):
                    no_correct += 1
                else:
                    no_incorrect += 1
                    print(f'商品货号：{productId}数据比对不上\n旧系统销售数量：{old_amount} 销售金额: {old_price}')
                    print(f'新系统销售数量：{new_amount} 销售金额: {new_price}')
            except ValueError:
                no_val_err += 1
                print(ValueError)
                print(
                    f'{ValueError}ind: {ind}商品货号：{productId}数据比对不上\n旧系统销售数量：{old_amount} 销售金额: {old_price}')
                print(f'新系统销售数量：{new_amount} 销售金额: {new_price}')
        print(
            f'交易流水项总数：{total}\n正确个数：{no_correct}\n交易流水项错误个数：{no_incorrect}\nindexErr: {no_index_err}\n valueErr: {no_val_err}')
