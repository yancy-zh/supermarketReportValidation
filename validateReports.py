#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
from stockReport import StockReport
from newStockReport import NewStockReport
from productInfo import ProductInfo


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
                print("expected string or bytes-like object, this line has wrong data")
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
                print("this line doesn't contain data")
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
        OLD_REPORT_FILENAME = r"6.6销售表.xls"
        NEW_REPORT_FILENAME = r"6 便利一店销售汇总.xls"
        # import excel sheets
        old_stock_report = StockReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_STOCK_REPORT_FILENAME,
                                       self._SHEET_NAME)
        df_stock_old_sys = old_stock_report.importExcelSheet()
        new_stock_report = NewStockReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_STOCK_REPORT_FILENAME)
        df_stock_new_sys = new_stock_report.importExcelSheet()