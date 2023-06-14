#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime

import pandas as pd

from stockReport import StockReport
from newStockReport import NewStockReport
from oldSaleReport import OldSaleReport
from newSaleReport import NewSaleReport
from oldTransactionRecordReport import OldTransactionRecordReport
from newSaleByCategoryReport import NewSaleByCategoryReport
from newTransactionReport import NewTransactionReport
from pandas import DataFrame
import math


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
        OLD_REPORT_FILENAME = r"6.6动态.xls"
        NEW_REPORT_FILENAME = r"4 商品进销存汇总表.xls"
        # import excel sheets

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
        categories = ["食用油", "调料", "副食", "大米", "面粉", "零食", "饮料", "副食", "乳制品", "蔬菜", "水果",
                      "蛋糕", "鸡蛋", "鸡蛋", "零食", "副食", "冻货", "大米", "乳制品", "副食", "食用油", "副食",
                      "乳制品酸奶", "乳制品纯奶", "食用油", "大米", "副食", "杂品类（购物袋）", "饮料", "副食", "调料",
                      "鸡蛋", "乳制品", "零食", "干货", "调料", "杂粮", "肉类", "冻货", "零食", "蛋糕", "副食"]
        for category in categories:
            old_sum_dict = old_report.getTotalByCategory(df_old_sys, category)
            new_sum_dict = new_report.getTotalByCategory(df_new_sys, category)
            if old_sum_dict == new_sum_dict:
                no_category_sum_correct += 1
            else:
                no_category_sum_incorrect += 1
                print(f'品类{category}数据对不上:\n - 旧系统：{old_sum_dict}\n- 新系统：{new_sum_dict}')

    def validateTransactionReports(self, name):
        print(f"运行{name}...")
        OLD_REPORT_FILENAME = r"6.6前台流水.xls"
        NEW_REPORT_FILENAME = r"9 前台商品销售流水.xls"
        no_nan = 0
        no_not_digit = 0
        no_correct =0
        no_incorrect =0

        # import excel sheets
        old_report = OldTransactionRecordReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                                self._SHEET_NAME)
        df_old_sys = old_report.importExcelSheet()
        new_report = NewTransactionReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME, self._SHEET_NAME)
        df_new_sys = new_report.importExcelSheet()
        total_line_num = df_old_sys.index.size
        df_old_sys_cleaned = old_report.cleanTable(df_old_sys)
        df_new_sys_cleaned = pd.DataFrame()
        for ind in df_old_sys.index:
            line_num = old_report.getLineNum(df_old_sys, ind)
            item_id = old_report.getItemId(df_old_sys, ind)
            try:
                if math.isnan(item_id):
                    no_nan += 1
                    print(f'nan')
                    continue
            except TypeError:
                if not old_report.isSerialNum(item_id):
                    no_not_digit += 1
                    print(f'str data')
                    continue
            try:
                if math.isnan(line_num):
                    no_nan += 1
                    print(f'nan')
                    continue
            except TypeError:
                if not old_report.isSerialNum(line_num):
                    no_not_digit+=1
                    print(f'str data')
                    continue
            old_transaction_it = old_report.getTransactionItem(df_old_sys, ind)
            new_transaction_it = old_report.getTransactionItem(df_new_sys, ind)
            if old_transaction_it == new_transaction_it:
                no_correct += 1
                print(f"商品货号正确：{line_num} 交易流水：\n旧系统: {old_transaction_it}, \n新系统: {new_transaction_it}")
            else:
                no_incorrect += 1
                print(f"商品货号錯誤：{line_num} 交易流水：\n旧系统: {old_transaction_it}, \n新系统: {new_transaction_it}")

            print(f'交易流水项正确个数：{no_correct}\n交易流水项错误个数：{no_incorrect}')
