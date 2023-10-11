#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import math

import pandas as pd

from comparator import Comparator
from importPurchaseStockGroupBySupplier import NewImportPurchaseStockGroupBySupplierReport
from importPurchaseStockGroupBySupplier import OldImportPurchaseStockGroupBySupplierReport
from newBasicInfoReport import NewBasicInfoReport
from newExportReport import NewExportReport
from newExportReportBySupplier import NewExportReportBySupplier
from newImportPurchaseStockReport import NewImportPurchaseStockReport
from newImportReport import NewImportReport
from newInventoryCountingReport import NewInventoryCountingReport
from newSaleByCategoryReport import NewSaleByCategoryReport
from newSaleReport import NewSaleReport
from newStockReport import NewStockReport
from newTransactionReport import NewTransactionReport
from oldBasicInfoReport import OldBasicInforReport
from oldExportReport import OldExportReport
from oldImportPurchaseStockReport import OldImportPurchaseStockReport
from oldImportReport import OldImportReport
from oldInventoryCountingReport import OldInventoryCountingReport
from oldSaleReport import OldSaleReport
from oldStockReport import OldStockReport
from oldTransactionRecordReport import OldTransactionRecordReport


class ValidateReports:
    _STOCK_VALIDATION_WORKING_DIR_OLD_SYS = r"D:\微云同步助手\89151701\liangli\proj\data\old\20230719-0722"
    _STOCK_VALIDATION_WORKING_DIR_NEW_SYS = r"D:\微云同步助手\89151701\liangli\proj\data\new\20230719-0722"
    _DATETIME_TO_VALIDATE = datetime.datetime(year=2023, month=7, day=25)
    _DATETIME_TODAY = datetime.datetime.today()
    _FORMAT_OF_PRINTED_DATE = "%Y-%m-%d"
    _SHEET_NAME = "Sheet1"

    def __init__(self):
        print(
            f'正在比对以下日期的数据 {self._DATETIME_TO_VALIDATE.__format__(self._FORMAT_OF_PRINTED_DATE)}')
        pass

    def validateStockReports(self, name):
        # compare two stock reports
        # parameters
        OLD_REPORT_FILENAME = r"7.18库存表.xls"
        NEW_REPORT_FILENAME = r"3 商品库存汇总报表 山东鲁花.xls"

        print(
            f"运行{name}，文件名：\n- {OLD_REPORT_FILENAME}\n- {NEW_REPORT_FILENAME}\n报告生成日期：{self._DATETIME_TODAY}...")
        # import excel sheets
        old_stock_report = OldStockReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                          self._SHEET_NAME)
        new_stock_report = NewStockReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME,
                                          self._SHEET_NAME)

        df_stock_old_sys = old_stock_report.importExcelSheet()
        df_stock_new_sys = new_stock_report.importExcelSheet()
        # clean tables
        df_stock_old_sys = old_stock_report.cleanTable(df_stock_old_sys, 1)
        df_stock_new_sys = new_stock_report.cleanTable(df_stock_new_sys, 1)
        # write data to csv
        df_stock_old_sys.to_csv(f'{name}old_stock_df_cleaned.csv')
        df_stock_new_sys.to_csv(f'{name}new_stock_df_cleaned.csv')

        # import csv to df
        df_stock_old_sys = pd.read_csv(f'{name}old_stock_df_cleaned.csv')
        df_stock_new_sys = pd.read_csv(f'{name}new_stock_df_cleaned.csv')
        # initialize counters
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
            if old_amount_str is math.nan:
                no_none_data += 1
                continue
            try:
                old_amount = old_stock_report.parseAmount(old_amount_str)
                if old_amount == 0:
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
            old_cost = old_stock_report.getCurrCost(df_stock_old_sys, tmp_productId)
            new_cost = new_stock_report.getCurrCost(df_stock_new_sys, tmp_productId)
            if old_cost == new_cost:
                no_cost_correct += 1
            elif old_cost != new_cost:
                no_cost_incorrect += 1
                print(f"商品 {tmp_productId} 的成本价核对不上，在旧系统中为：{old_cost}，在新系统中为{new_cost}")
            # check salePrice
            old_sale_price = old_stock_report.getCurrSalePrice(df_stock_old_sys, tmp_productId)
            new_salePrice = new_stock_report.getCurrSalePrice(df_stock_new_sys, tmp_productId)
            if old_sale_price == new_salePrice:
                no_sale_price_correct += 1
            elif old_sale_price != new_salePrice:
                no_sale_price_incorrect += 1
                print(f"商品 {tmp_productId} 的销售价核对不上，在旧系统中为：{old_cost}，在新系统中为{new_salePrice}")
        print(
            f'{name} ended...\n总处理行数: {total_line_num} 个\n数量正确: {no_amount_correct} 个\n数量为零: {no_zero_amount}\n无数据: {no_none_data} 个\n')
        print(f'成本价正确: {no_cost_correct} 个\n成本价错误: {no_cost_incorrect} 个\n')
        print(f'销售价正确: {no_sale_price_correct} 个\n销售价错误: {no_sale_price_incorrect} 个\n')

    def validatePurchaseSaleStockReports(self, name):
        OLD_REPORT_FILENAME = r"7.19-7.22动态明细.xls"
        NEW_REPORT_FILENAME = r"4 商品进销存汇总表 臻泽.xls"
        print(
            f"运行比对{name}，文件名：\n- {OLD_REPORT_FILENAME}\n- {NEW_REPORT_FILENAME}\n报告生成日期：{self._DATETIME_TODAY}...")
        no_correct = 0
        no_incorrect = 0
        # initialize objs
        report_old = OldImportPurchaseStockReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                                  self._SHEET_NAME)
        report_new = NewImportPurchaseStockReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME,
                                                  self._SHEET_NAME)
        # import excel sheets
        df_old = report_old.importExcelSheet()
        df_new = report_new.importExcelSheet()
        # # clean up the table
        df_old = report_old.cleanTable(df_old, 0)
        df_new = report_new.cleanTable(df_new, 0)
        # # write data to csv
        df_old.to_csv(f'{name}old_report_cleaned.csv')
        df_new.to_csv(f'{name}new_report_cleaned.csv')

        # import csv to df
        df_old = pd.read_csv(f"{name}old_report_cleaned.csv")
        df_new = pd.read_csv(f"{name}new_report_cleaned.csv")
        # convert text data to digital
        df_old = report_old.convertTextDataToDigital(df_old)
        df_new = report_new.convertTextDataToDigital(df_new)
        # loop in the table
        for ind in df_new.index:
            serial_num = df_new['serialNum'][ind]
            if serial_num in report_new.EXCLUDED_SERIAL_NUMS:
                continue
            old_dict = report_old.getRowByKey(df_old, serial_num)
            new_dict = report_new.getRowByKey(df_new, serial_num)
            if report_old.compareDicts(old_dict, new_dict):
                no_correct += 1
            else:
                no_incorrect += 1
                print(f'商品：{serial_num}数据对不上:\n - 旧系统：{old_dict.values}\n- 新系统：{new_dict.values}')
        print(f'总数据行数：{len(df_new)}')
        print(f'数据正确共：{no_correct}\n数据错误共：{no_incorrect}')

    def validateSaleReports(self, name):
        print(f"运行{name}，日期：{self._DATETIME_TODAY}...")
        OLD_REPORT_FILENAME = r"7.19-7.22销售明细.xls"
        NEW_REPORT_FILENAME = r"7 便利一店销售汇总报表 臻泽.xls"  # 7 便利一店销售汇总报表-按品名排序（0919导）
        print(
            f"运行{name}，文件名：\n-{OLD_REPORT_FILENAME}\n-{NEW_REPORT_FILENAME}\n日期：{self._DATETIME_TODAY}...")
        # import excel sheets
        old_report = OldSaleReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                   self._SHEET_NAME)
        new_report = NewSaleReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME, self._SHEET_NAME)
        df_old = old_report.importExcelSheet()
        df_new = new_report.importExcelSheet()
        # # clean up the table
        df_old = old_report.cleanTable(df_old, 0)
        df_new = new_report.cleanTable(df_new, 0)
        # # write data to csv
        df_old.to_csv(f'{name}old_report_cleaned.csv')
        df_new.to_csv(f'{name}new_report_cleaned.csv')
        # import csv to df
        df_old = pd.read_csv(f'{name}old_report_cleaned.csv')
        df_new = pd.read_csv(f'{name}new_report_cleaned.csv')
        # 表总行数
        total_line_num = df_new.index.size  # df_old.index.size
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
        for ind in df_new.index:
            serial_num = new_report.getSerialNum(df_new, ind)
            try:
                old_sale_amount = old_report.getSaleAmount(df_old, serial_num)
            except TypeError:
                print("旧系统表中该行包含错误数据")
                continue
            new_sale_amount = new_report.getSaleAmount(df_new, serial_num)
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
                old_refund_amount = old_report.getRefundAmount(df_old, serial_num)
            except TypeError:
                print("旧系统表中该行包含错误数据")
                continue
            new_refund_amount = new_report.getRefundAmount(df_new, serial_num)
            if new_refund_amount == -old_refund_amount:
                no_refund_amount_correct += 1
            else:
                no_refund_amount_incorrect += 1
                print(
                    f"商品 {serial_num} 的退貨数量核对不上，在旧系统中为：{old_refund_amount}，在新系统中为{new_refund_amount}")
            # compare sale price
            old_sale_price = old_report.getSalePrice(df_old, serial_num)
            new_sale_price = new_report.getSaleTotal(df_new, serial_num)
            if old_sale_price == new_sale_price:
                no_sale_price_correct += 1
            else:
                no_sale_price_incorrect += 1
                print(
                    f"商品 {serial_num} 的销售金额核对不上，在旧系统中为：{old_sale_price}，在新系统中为{new_sale_price}")
            # compare refund price
            old_refund_price = old_report.getRefundPrice(df_old, serial_num)
            new_refund_price = new_report.getRefundPrice(df_new, serial_num)
            if old_refund_price == -new_refund_price:
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
        OLD_REPORT_FILENAME = r"7.19-7.22销售明细.xls"
        NEW_REPORT_FILENAME = r"7 便利一店销售汇总报表 - 品类排序7.20-7.25.xls"
        no_category_sum_correct = 0
        no_category_sum_incorrect = 0
        # import excel sheets
        old_report = OldSaleReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                   self._SHEET_NAME)
        df_old = old_report.importExcelSheet()
        new_report = NewSaleByCategoryReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME,
                                             self._SHEET_NAME)
        df_new = new_report.importExcelSheet()
        # # # clean up the table
        # df_old = old_report.cleanTable(df_old, 0)
        # df_new = new_report.cleanTable(df_new, 0)
        ls = ["食用油", "调料", "副食", "大米", "面粉", "零食", "饮料", "副食", "乳制品", "蔬菜", "水果"
            , "鸡蛋", "乳制品酸奶", "乳制品纯奶", "杂品类（购物袋）", "调料"
            , "干货", "杂粮", "肉类", "冻货", "蛋糕", "腊肉类"]
        categories = set(ls)
        for category in categories:
            old_sum_dict = old_report.getTotalByCategory(df_old, category)
            new_sum_dict = new_report.getTotalByCategory(df_new, category)
            if old_sum_dict == new_sum_dict:
                no_category_sum_correct += 1
            else:
                no_category_sum_incorrect += 1
                print(f'品类{category}数据对不上:\n - 旧系统：{old_sum_dict}\n- 新系统：{new_sum_dict}')
        print(f"品类数量共：{len(categories)}\n分别是：{categories}")
        print(f'数据正确共：{no_category_sum_correct}\n数据错误共：{no_category_sum_incorrect}')

    def validateTransactionReports(self, name):
        print(f"运行{name}，日期：{self._DATETIME_TODAY}...")
        OLD_REPORT_FILENAME = r"7.19-7.22流水.xls"
        NEW_REPORT_FILENAME = r"9 前台商品销售流水（0831导）.xls"
        print(
            f"运行{name}，文件名：\n- {OLD_REPORT_FILENAME}\n- {NEW_REPORT_FILENAME}\n日期：{self._DATETIME_TODAY}...")

        # import excel sheets
        old_report = OldTransactionRecordReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                                self._SHEET_NAME)
        df_old_sys = old_report.importExcelSheet()
        new_report = NewTransactionReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME,
                                          self._SHEET_NAME)
        df_new_sys = new_report.importExcelSheet()
        df_old_sys_cleaned = old_report.cleanTable(df_old_sys, 2)
        df_old_sys_cleaned = old_report.convertTextDataToDigital(df_old_sys_cleaned)
        df_old_sys_cleaned = old_report.flipRefundAmountSign(df_old_sys_cleaned)
        df_old_sys_amount_sum = old_report.calAmountSummary(df_old_sys_cleaned)
        df_old_sys_amount_sum.to_csv(f'{name}df_old_sys_amount_sum.csv')
        df_new_sys_cleaned = new_report.cleanTable(df_new_sys, 2)
        df_new_sys_amount_sum = new_report.calAmountSummary(new_report.convertTextDataToDigital(df_new_sys_cleaned))
        df_new_sys_amount_sum.to_csv(f'{name}df_new_sys_amount_sum.csv')

    def compareTransactionReports(self, name):
        # TODO: 加销售类型字段
        print(f'运行：{name}')
        df_old = pd.read_csv(f'{name}df_old_sys_amount_sum.csv')
        df_new = pd.read_csv(f'{name}df_new_sys_amount_sum.csv')
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
                    f'{IndexError}ind: {ind}\n商品货号：{productId}数据比对不上\n旧系统销售数量：{old_amount} 销售金额: {old_price}')
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
                    f'{ValueError}ind: {ind}\n商品货号：{productId}数据比对不上\n旧系统销售数量：{old_amount} 销售金额: {old_price}')
                print(f'新系统销售数量：{new_amount} 销售金额: {new_price}')
        print(
            f'交易流水项总数：{total}\n正确个数：{no_correct}\n交易流水项错误个数：{no_incorrect}\nindexErr: {no_index_err}\n valueErr: {no_val_err}')

    def validateImportReports_generateCSVs(self, name, supplierName):
        print(f'运行生成CSV：{name}-{supplierName}')
        OLD_REPORT_FILENAME = f'6.6{supplierName}.xls'
        NEW_REPORT_FILENAME = r"13 便利一店入库单.xls"

        # import excel sheets
        old_report = OldImportReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                     self._SHEET_NAME)
        new_report = NewImportReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME,
                                     self._SHEET_NAME)
        df_old = old_report.importExcelSheet()
        df_new = new_report.importExcelSheet()
        df_old = old_report.cleanTableWOUnited(df_old)
        df_new = new_report.cleanTableWOUnited(df_new)
        df_old = old_report.convertTextDataToDigital(df_old)
        df_new = new_report.convertTextDataToDigital(df_new)
        df_old.to_csv(f'{name}_{supplierName}_df_old_sys.csv')
        df_new.to_csv(f'{name}_{supplierName}_df_new_sys.csv')

    def validateImportReportsBySupplier(self, name, supplier_name):
        OLD_REPORT_FILENAME = f'7.19-7.22入库明细{supplier_name}.xls'
        NEW_REPORT_FILENAME = f"13 便利一店入库单 {supplier_name}.xls"
        program_name = "程序" + name + "来自供应商：" + supplier_name
        comparator = Comparator(OLD_REPORT_FILENAME, NEW_REPORT_FILENAME, program_name, self._DATETIME_TODAY)
        comparator.printLogHeaderOldAndNew()
        # import excel sheets
        old_report = OldImportReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                     self._SHEET_NAME)
        new_report = NewImportReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME,
                                     self._SHEET_NAME)
        df_old = old_report.importExcelSheet()
        df_new = new_report.importExcelSheet()
        df_old = old_report.cleanTableWOUnited(df_old)
        df_new = new_report.cleanTableWOUnited(df_new)
        df_old = old_report.convertTextDataToDigital(df_old)
        df_new = new_report.convertTextDataToDigital(df_new)
        csv_prefix = f'{program_name}_{supplier_name}'
        comparator.saveToCsvs(df_old, df_new, csv_prefix)
        [df_old, df_new] = comparator.loadCsvsToDataframe(csv_prefix)
        total = len(df_old.index)
        no_correct = 0
        no_incorrect = 0
        for ind in df_old.index:
            serial_num = df_old['serialNum'][ind]
            old_dict = old_report.getRowByKey(df_old, serial_num)
            new_dict = new_report.getRowByKey(df_new, serial_num)
            if old_report.compareDicts(old_dict, new_dict):
                no_correct += 1
            else:
                no_incorrect += 1
                comparator.printItemUnequalResult(serial_num, old_dict, new_dict)
        comparator.printTotalResult(total, no_correct, no_incorrect)

    def validateImportReports_compareCSVs(self, name, supplierName):
        print(f'运行比对CSV：{name}-{supplierName}')
        OLD_REPORT_FILENAME = f'6.6{supplierName}.xls'
        NEW_REPORT_FILENAME = r"13 便利一店入库单.xls"
        # import excel sheets
        old_report = OldImportReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                     self._SHEET_NAME)
        new_report = NewImportReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME,
                                     self._SHEET_NAME)
        df_old = pd.read_csv(f'{name}_{supplierName}_df_old_sys.csv')
        df_new = pd.read_csv(f'{name}_{supplierName}_df_new_sys.csv')
        total = len(df_old.index)
        no_correct = 0
        no_incorrect = 0
        for ind in df_old.index:
            serial_num = df_old['serialNum'][ind]
            old_dict = old_report.getRowByKey(df_old, serial_num)
            new_dict = new_report.getRowByKey(df_new, serial_num)
            if old_report.compareDicts(old_dict, new_dict):
                no_correct += 1
            else:
                no_incorrect += 1
                print(f'商品：{serial_num}数据对不上:\n - 旧系统：{old_dict.values}\n- 新系统：{new_dict.values}')
        print(f'总数据行数：{total}')
        print(f'数据正确共：{no_correct}\n数据错误共：{no_incorrect}')

    def validateImportReports(self, name):
        SUPPLIERS = ['傲涵', '超乐惠', '丰泰', '和天熙', '蓝鲁', '品优兴', '腾旺',
                     '小大', '一生一客', '秦南', '三炫', '西华', '丹君', '老牛', '臻泽', '米脂', '海和景', '野森林',
                     '菲达', '鲁花', '其林', '永信']
        for supplier in SUPPLIERS:
            try:
                self.validateImportReportsBySupplier(name, supplier)
            #     TODO: 显示哪个系统
            except FileNotFoundError:
                print(f"{supplier} 无入库单。")
                continue
        # for supplier in SUPPLIERS:
        #     self.validateImportReports_generateCSVs(name, supplier)
        # for supplier in SUPPLIERS:
        #     self.validateImportReports_compareCSVs(name, supplier)

    def validateImportPurchaseStockGroupBySupplier(self, name):
        print(f'运行比对：{name}')
        OLD_REPORT_FILENAME = f'7.19-7.22进销存变动表-删掉为零的.xls'
        NEW_REPORT_FILENAME = r"G05 商品进销存变动表 - 230818.xls"
        print(
            f"运行{name}，文件名：\n-{OLD_REPORT_FILENAME}\n-{NEW_REPORT_FILENAME}\n日期：{self._DATETIME_TODAY}...")
        # import excel sheets
        old_report = OldImportPurchaseStockGroupBySupplierReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS,
                                                                 OLD_REPORT_FILENAME,
                                                                 self._SHEET_NAME)
        new_report = NewImportPurchaseStockGroupBySupplierReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS,
                                                                 NEW_REPORT_FILENAME,
                                                                 self._SHEET_NAME)
        df_old = old_report.importExcelSheet()
        df_new = new_report.importExcelSheet()
        df_old = old_report.cleanTableNotSupplier(df_old)
        df_new = old_report.cleanTableNotSupplier(df_new)
        df_old = old_report.convertTextDataToDigital(df_old)
        df_new = new_report.convertTextDataToDigital(df_new)
        total = len(df_new.index)
        no_correct = 0
        no_incorrect = 0
        for ind in df_new.index:
            supplier_name = df_new['supplierName'][ind]
            old_dict = old_report.getRowByKey(df_old, supplier_name)
            new_dict = new_report.getRowByKey(df_new, supplier_name)
            if old_report.compareDicts(old_dict, new_dict):
                no_correct += 1
            else:
                no_incorrect += 1
                print(f'商品：{supplier_name}数据对不上:\n - 旧系统：{old_dict.values}\n- 新系统：{new_dict.values}')
        print(f'总数据行数：{total}')
        print(f'数据正确共：{no_correct}\n数据错误共：{no_incorrect}')

    def validateInventoryCountingReports(self, name):
        print(f'运行比对：{name}')
        OLD_REPORT_FILENAME = f'7.22盘点差异表.xls'
        NEW_REPORT_FILENAME = r'1 盘点差异表 - 盈亏分组(0908导).xls'
        print(
            f"运行{name}，文件名：\n- {OLD_REPORT_FILENAME}\n- {NEW_REPORT_FILENAME}\n报告生成日期：{self._DATETIME_TODAY}...")
        # import excel sheets
        old_report = OldInventoryCountingReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                                self._SHEET_NAME)
        new_report = NewInventoryCountingReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME,
                                                self._SHEET_NAME)
        df_old = old_report.importExcelSheet()
        df_new = new_report.importExcelSheet()
        # # clean up the table
        # df_old = old_report.cleanTable(df_old, 0)
        # df_new = new_report.cleanTable(df_new, 0)
        # convert text data to digital
        # df_old = old_report.convertTextDataToDigital(df_old)
        # df_new = new_report.convertTextDataToDigital(df_new)
        # write data to csv
        # df_old.to_csv(f'{name}old_report_cleaned.csv')
        # df_new.to_csv(f'{name}new_report_cleaned.csv')
        # import csv to df
        df_old = pd.read_csv(f'{name}old_report_cleaned.csv')
        df_new = pd.read_csv(f'{name}new_report_cleaned.csv')
        total = len(df_new.index)
        no_correct = 0
        no_incorrect = 0
        for ind in df_new.index:
            serial_num = df_new['serialNum'][ind]
            old_dict = old_report.getRowByKey(df_old, serial_num)
            new_dict = new_report.getRowByKey(df_new, serial_num)
            if new_report.compareDicts(old_dict, new_dict):
                no_correct += 1
            else:
                no_incorrect += 1
                print(f'商品：{serial_num}数据对不上:\n - 旧系统：{old_dict.values}\n- 新系统：{new_dict.values}')
        print(f'总数据行数：{total}')
        print(f'数据正确共：{no_correct}\n数据错误共：{no_incorrect}')

    def cleanUpReport(self, name):
        print(f'运行：{name}')
        OLD_REPORT_FILENAME = f'7.18库存表.xls'
        old_report = OldStockReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                    self._SHEET_NAME)
        df_old = old_report.importExcelSheet()
        df_united = old_report.filterUnitedProducts(df_old)
        df_united.to_csv(f'{name}_联营商品.csv')

    def checkStockAndImportPurchase(self, name):
        OLD_STOCK_REPORT_FILENAME = r"7.18库存表.xls"
        NEW_STOCK_REPORT_FILENAME = r"4 商品进销存汇总表-0826.xls"
        no_correct = 0
        no_incorrect = 0
        print(
            f'Hi, {name} for date {self._DATETIME_TO_VALIDATE.__format__(self._FORMAT_OF_PRINTED_DATE)}')  # Press Ctrl+Shift+B to toggle the breakpoint.
        # import excel sheets
        old_report = OldStockReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_STOCK_REPORT_FILENAME,
                                    self._SHEET_NAME)
        new_report = NewImportPurchaseStockReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_STOCK_REPORT_FILENAME,
                                                  self._SHEET_NAME)
        # df_old = old_report.importExcelSheet()
        # df_new = new_report.importExcelSheet()
        # # clean tables
        # df_old = old_report.cleanTable(df_old, 1)
        # df_new = new_report.cleanTable(df_new, 1)
        # # write data to csv
        # df_old.to_csv(f'{name}old_stock_df_cleaned.csv')
        # df_new.to_csv(f'{name}new_import_purchase_stock_df_cleaned.csv')
        # import csv to df
        df_old = pd.read_csv(f'{name}old_stock_df_cleaned.csv')
        df_new = pd.read_csv(f'{name}new_import_purchase_stock_df_cleaned.csv')
        # loop in the table
        for ind in df_new.index:
            serial_num = df_new['serialNum'][ind]
            old_dict = old_report.getRowByKey(df_old, serial_num)
            new_dict = new_report.getRowByKey(df_new, serial_num)
            try:
                old_amount = old_report.parseAmount(old_dict.values[0, 1])
            except IndexError:
                print(f'商品：{serial_num} 数据对不上，在旧系统中不存在或库存为0')
                no_incorrect += 1
                continue
            try:
                new_amount = new_report.parseAmount(new_dict.values[0, 5])
            except IndexError:
                print(f'商品：{serial_num} 数据对不上，在新系统中不存在或库存为0')
                no_incorrect += 1
                continue
            if old_amount == new_amount:
                no_correct += 1
            else:
                no_incorrect += 1
                print(f'商品：{serial_num}数据对不上:\n - 旧系统：{old_amount}\n- 新系统：{new_amount}')
        print(f'总数据行数：{len(df_new)}')
        print(f'数据正确共：{no_correct}\n数据错误共：{no_incorrect}')

    def validateBasicInfoReports(self, name):
        OLD_REPORT_FILENAME = r"7.18z商品一览表.xls"
        NEW_REPORT_FILENAME = r"商品一览表.xlsx"
        print(
            f"运行{name}，文件名：\n-{OLD_REPORT_FILENAME}\n-{NEW_REPORT_FILENAME}\n日期：{self._DATETIME_TODAY}...")
        # import excel sheets
        old_report = OldBasicInforReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                         self._SHEET_NAME)
        new_report = NewBasicInfoReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME,
                                        self._SHEET_NAME)
        # df_old = old_report.importExcelSheet()
        # df_new = new_report.importExcelSheet()
        # # # clean up the table
        # df_old = old_report.cleanTable(df_old, 2)
        # df_new = new_report.cleanTable(df_new, 1)
        # # # write data to csv
        # df_old.to_csv(f'{name}old_report_cleaned.csv')
        # df_new.to_csv(f'{name}new_report_cleaned.csv')
        # import csv to df
        df_old = pd.read_csv(f'{name}old_report_cleaned.csv')
        df_new = pd.read_csv(f'{name}new_report_cleaned.csv')
        # loop in the table
        total = len(df_new.index)
        no_correct = 0
        no_incorrect = 0
        for ind in df_new.index:
            serial_num = df_new['serialNum'][ind]
            old_dict = old_report.getRowByKey(df_old, serial_num)
            new_dict = new_report.getRowByKey(df_new, serial_num)
            if new_report.compareDicts(old_dict, new_dict):
                no_correct += 1
            else:
                no_incorrect += 1
                print(f'商品：{serial_num}数据对不上:\n - 旧系统：{old_dict.values}\n- 新系统：{new_dict.values}')
        print(f'总数据行数：{total}')
        print(f'数据正确共：{no_correct}\n数据错误共：{no_incorrect}')

    def validateSaleAndImportPurchaseStock(self, name):
        REPORT1_FILENAME = r"7 便利一店销售汇总报表（0905导）.xls"
        REPORT2_FILENAME = r"G04 商品进销存汇总表 - 230818.xls"
        BASIC_INFO_FILENAME = r"商品一览表.xlsx"
        print(
            f"运行{name}，文件名：\n- {REPORT1_FILENAME}\n- {REPORT2_FILENAME}\n- {BASIC_INFO_FILENAME}\n日期：{self._DATETIME_TODAY}...")
        # import excel sheets
        report1 = NewSaleReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, REPORT1_FILENAME,
                                self._SHEET_NAME)
        report1.SELECTED_COL_NAMES = ['serialNum', 'saleAmount', 'saleTotal', 'refundAmount', 'refundPrice', 'cost',
                                      'salePrice']
        report1.SELECTED_COL_IDS = 'E, N, O, P, R, T, U'
        report2 = NewImportPurchaseStockReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, REPORT2_FILENAME,
                                               self._SHEET_NAME)
        basic_info_report = NewBasicInfoReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, BASIC_INFO_FILENAME,
                                               self._SHEET_NAME)
        # df_1 = report1.importExcelSheet()
        # df_2 = report2.importExcelSheet()
        # df_3 = basic_info_report.importExcelSheet()
        # clean up the table
        # df_1 = report1.cleanTable(df_1, 0)
        # df_2 = report2.cleanTable(df_2, 0)
        # df_3 = basic_info_report.cleanTable(df_3, 1)
        # # write data to csv
        # df_1.to_csv(f'{name}report1_cleaned.csv')
        # df_2.to_csv(f'{name}report2_cleaned.csv')
        # df_3.to_csv(f'{name}report3_cleaned.csv')
        # import csv to df
        df_1 = pd.read_csv(f'{name}report1_cleaned.csv')
        df_2 = pd.read_csv(f'{name}report2_cleaned.csv')
        df_3 = pd.read_csv(f'{name}report3_cleaned.csv')
        # loop in the table
        total = len(df_1.index)
        no_correct = 0
        no_incorrect = 0
        for ind in df_1.index:
            serial_num = df_1['serialNum'][ind]
            saleAmount_1 = report1.getSaleAmount(df_1, serial_num) + report1.getRefundAmount(df_1, serial_num)
            saleAmount_2 = -1
            try:
                saleAmount_2 = report2.getRowByKey(df_2, serial_num)['saleAmount'].values[0]
            except IndexError:
                print(f"该商品在进销存表中不存在：{serial_num}")

            dict_1 = report1.getRowByKey(df_1, serial_num)
            dict_2 = report2.getRowByKey(df_2, serial_num)
            dict_3 = df_3[df_3['serialNum'] == serial_num]
            try:  # 进销存表调用成本价
                cost_import_purchase = dict_2['preSaleCost'].values[0]
            except IndexError:
                cost_import_purchase = -1
                print(f'该商品在进销存表中不存在.')
            try:  # 商品一览表调用成本价
                cost_basic_info = dict_3['cost'].values[0]
            except IndexError:
                cost_basic_info = -1
                print(f"该商品在商品一览表中不存在.")
            try:  # 销售表调用售价
                sale_price_sale_summary = dict_1['salePrice'].values[0]
            except IndexError:
                sale_price_sale_summary = -1
                print(f"该商品在销售表中不存在.")
            try:  # 商品一览表调用售价
                sale_price_basic_info = dict_3['currPrice'].values[0]
            except IndexError:
                sale_price_basic_info = -1
                print(f"该商品在商品一览表中不存在.")

            # 核对进销存表里的销售数量、进价
            if saleAmount_1 == saleAmount_2 \
                    and cost_basic_info == cost_import_purchase \
                    and sale_price_basic_info == float(sale_price_sale_summary):
                no_correct += 1
            else:
                no_incorrect += 1
                print(f'商品：{serial_num}数据对不上:\n 数量 - 表1：{saleAmount_1}，- 表2：{saleAmount_2}')
                print(f'进价 - 表2：{cost_import_purchase}，- 表3：{cost_basic_info}')
                print(f'售价 - 表1：{sale_price_sale_summary}，- 表3：{sale_price_basic_info}')
                continue
        print(f'总数据行数：{total}')
        print(f'数据正确共：{no_correct}\n数据错误共：{no_incorrect}')

    def validateSaleAndExport(self, name):
        REPORT1_FILENAME = r"7 便利一店销售汇总报表（0905导）.xls"
        REPORT2_FILENAME = r"8 便利一店出库汇总明细（0913）.xls"
        BASIC_INFO_FILENAME = r"商品一览表.xlsx"

        print(
            f"运行{name}，文件名：\n- {REPORT1_FILENAME}\n- {REPORT2_FILENAME}\n- {BASIC_INFO_FILENAME}\n日期：{self._DATETIME_TODAY}...")
        # import excel sheets
        report1 = NewSaleReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, REPORT1_FILENAME,
                                self._SHEET_NAME)
        report1.SELECTED_COL_NAMES = ['serialNum', 'saleAmount', 'saleTotal', 'refundAmount', 'refundPrice', 'cost',
                                      'salePrice']
        report1.SELECTED_COL_IDS = 'E, N, O, P, R, T, U'
        report2 = NewExportReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, REPORT2_FILENAME,
                                  self._SHEET_NAME)
        basic_info_report = NewBasicInfoReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, BASIC_INFO_FILENAME,
                                               self._SHEET_NAME)

        # df_1 = report1.importExcelSheet()
        # df_2 = report2.importExcelSheet()
        # df_3 = basic_info_report.importExcelSheet()
        # clean up the table
        # df_1 = report1.cleanTable(df_1, 0)
        # df_2 = report2.cleanTable(df_2, 1)
        # df_3 = basic_info_report.cleanTable(df_3, 1)
        # write data to csv
        # df_1.to_csv(f'{name}report1_cleaned.csv')
        # df_2.to_csv(f'{name}report2_cleaned.csv')
        # df_3.to_csv(f'{name}report3_cleaned.csv')
        # import csv to df
        df_1 = pd.read_csv(f'{name}report1_cleaned.csv')
        df_2 = pd.read_csv(f'{name}report2_cleaned.csv')
        df_3 = pd.read_csv(f'{name}report3_cleaned.csv')
        # loop in the table
        total = len(df_1.index)
        no_correct = 0
        no_incorrect = 0
        for ind in df_1.index:
            serial_num = df_1['serialNum'][ind]
            # 核对销售表和出库汇总表里的销售数量、进价
            saleAmount_1 = report1.getSaleAmount(df_1, serial_num) + report1.getRefundAmount(df_1, serial_num)
            saleAmount_2 = -1
            try:
                saleAmount_2 = report2.getRowByKey(df_2, serial_num)['saleAmount'].values[0]
            except IndexError:
                print(f"该商品在出库汇总明细表中不存在：{serial_num}")
            # 核对销售表和出库汇总表里的销售收入，销售成本
            salePrice_1 = report1.getSaleTotal(df_1, serial_num) + report1.getRefundPrice(df_1, serial_num)
            salePrice_2 = -1
            try:
                salePrice_2 = report2.getSalePrice(df_2, serial_num)
            except IndexError:
                print(f"该商品在出库汇总明细表中不存在：{serial_num}")
            # 核对出库汇总表里的销售毛利率
            totalCost_2 = report2.getTotalCost(df_2, serial_num)
            grossProfit_2 = report2.getGrossProfit(df_2, serial_num)
            if saleAmount_1 == saleAmount_2 \
                    and salePrice_1 == salePrice_2 \
                    and round(salePrice_2 - totalCost_2, 2) == round(grossProfit_2, 2):
                no_correct += 1
            else:
                no_incorrect += 1
                print(f'商品：{serial_num}数据对不上:\n 数量 - 表1：{saleAmount_1}，- 表2：{saleAmount_2}')
                print(f'销售收入 - 表1：{salePrice_1}，- 表2：{salePrice_2}')
                print(f'销售收入、成本、毛利率 - 表2：{salePrice_2}，{totalCost_2}, {grossProfit_2}')
        print(f'总数据行数：{total}')
        print(f'数据正确共：{no_correct}\n数据错误共：{no_incorrect}')

    def validateExportReport(self, name):
        REPORT2_FILENAME = r"8 便利一店出库汇总明细（0913）.xls"
        REPORT4_FILENAME = r"7.19-7.22出库.xls"
        print(
            f"运行{name}，文件名：\n- {REPORT4_FILENAME}\n- {REPORT2_FILENAME}\n日期：{self._DATETIME_TODAY}...")
        # import excel sheets
        report2 = NewExportReport(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, REPORT2_FILENAME,
                                  self._SHEET_NAME)
        report4 = OldExportReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, REPORT4_FILENAME,
                                  self._SHEET_NAME)
        df_2 = report2.importExcelSheet()
        df_4 = report4.importExcelSheet()
        # clean up the table
        df_2 = report2.cleanTable(df_2, 1)
        df_4 = report4.cleanTableNotSupplier(df_4)
        df_4 = report4.convertTextDataToDigital(df_4)
        # write data to csv
        df_2.to_csv(f'{name}report2_cleaned.csv')
        df_4.to_csv(f'{name}report4_cleaned.csv')
        # import csv to df
        df_2 = pd.read_csv(f'{name}report2_cleaned.csv')
        df_4 = pd.read_csv(f'{name}report4_cleaned.csv')
        # loop in the table
        total = len(df_4.index)
        no_correct = 0
        no_incorrect = 0
        # 核对新旧系统出库表
        groupby_obj = report2.calAmountSummary(df_2)
        for ind in df_4.index:
            supplier_name = report4.getSupplierName(df_4, ind)
            category_name = report4.getCategoryName(df_4, ind)
            sale_amount_4 = report4.getSaleAmount(df_4, ind)
            sale_income_4 = report4.getSaleIncome(df_4, ind)
            try:
                group_in_report2 = groupby_obj.get_group((supplier_name, category_name))
                group_sale_amount = group_in_report2['saleAmount'].sum()
                group_income = round(group_in_report2['saleIncome'].sum(), 2)
            except KeyError:
                print(f"{supplier_name},{category_name}在新系统中不存在。")
                group_sale_amount = -1
                group_income = -1
            if group_sale_amount == sale_amount_4 \
                    and group_income == sale_income_4:
                no_correct += 1
            else:
                no_incorrect += 1
                print(f'组别：{supplier_name},{category_name}数据对不上:\n'
                      f' 销售数量、销售收入 - 旧系统：{sale_amount_4}，{sale_income_4}，'
                      f'- 新系统：{group_sale_amount}，{group_income}')
        print(f'总数据行数：{total}')
        print(f'数据正确共：{no_correct}\n数据错误共：{no_incorrect}')

    def validateExportReportBySupplier(self, name):
        NEW_REPORT_FILENAME = r"8 便利一店出库汇总明细 丹君.xls"
        OLD_REPORT_FILENAME = r"7.19-7.22出库.xls"
        print(
            f"运行{name}，文件名：\n- {OLD_REPORT_FILENAME}\n- {NEW_REPORT_FILENAME}\n日期：{self._DATETIME_TODAY}...")
        # import excel sheets
        new_report = NewExportReportBySupplier(self._STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_REPORT_FILENAME,
                                               self._SHEET_NAME)
        old_report = OldExportReport(self._STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_REPORT_FILENAME,
                                     self._SHEET_NAME)
        df_new = new_report.importExcelSheet()
        df_old = old_report.importExcelSheet()
        # clean up the table
        df_new = new_report.cleanTable(df_new, 1)
        df_old = old_report.cleanTableNotSupplier(df_old)
        df_old = old_report.convertTextDataToDigital(df_old)
        # write data to csv
        df_new.to_csv(f'{name}report2_cleaned.csv')
        df_old.to_csv(f'{name}report4_cleaned.csv')
        # import csv to df
        df_new = pd.read_csv(f'{name}report2_cleaned.csv')
        df_old = pd.read_csv(f'{name}report4_cleaned.csv')
        # get the supplier name
        supplier_name_new = new_report.getSupplierName(df_new)
        # filter the table of old report
        df_old_filtered_supplier = df_old[df_old['supplierName'] == supplier_name_new]
        # loop in the table
        total = len(df_old_filtered_supplier.index)
        no_correct = 0
        no_incorrect = 0
        # 核对新旧系统出库表
        groupby_obj = new_report.calAmountSummary(df_new)
        for ind in range(total):
            dict_old = df_old_filtered_supplier.iloc[ind].to_dict()
            category_name = dict_old['categoryName']
            try:
                dict_new = new_report.getAllStatsForGroup(groupby_obj, supplier_name_new, category_name)
                dict_old['grossProfitRate'] = old_report.rateToDecimal(dict_old['grossProfitRate'])
                if old_report.compareDicts(dict_old, dict_new):
                    no_correct += 1
                else:
                    no_incorrect += 1
                    print(f'组别：{supplier_name_new},{category_name}数据对不上:\n'
                          f' - 旧系统：{dict_old}\n'
                          f'- 新系统：{dict_new}')
            except Exception:
                print(f"{supplier_name_new},{category_name}在新系统中不存在。")
        print(f'总数据行数：{total}')
        print(f'数据正确共：{no_correct}\n数据错误共：{no_incorrect}')
