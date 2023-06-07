# This is a sample Python script.
# coding=utf-8
import datetime
import sys

# Press Alt+Shift+X to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from stockReport import StockReport


def run(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+Shift+B to toggle the breakpoint.
    # parameters
    STOCK_VALIDATION_WORKING_DIR_OLD_SYS = r"D:\微云同步助手\89151701\liangli\proj\data\old\20230315"
    STOCK_VALIDATION_WORKING_DIR_NEW_SYS = r"D:\微云同步助手\89151701\liangli\proj\data\new\20230315\3.16-3.17朝阳门便利一店测试汇总"
    OLD_STOCK_REPORT_FILENAME = r"3.14库存.xls"
    NEW_STOCK_REPORT_FILENAME = r"3 商品库存汇总报表.xls"
    SHEET_NAME = "Sheet1"
    SELECTED_COL_IDS_OLD_SYS = r'D, E, G, I, J, L'
    SELECTED_COL_IDS_NEW_SYS = r'C, D, E, I, K, O'
    SELECTED_COL_NAMES = ["categoryName", "productId", "productName", "amount", "currCost", "salePrice"]
    DATETIME_TO_VALIDATE = datetime.datetime(year=2023, month=3, day=15)

    # import excel sheets
    old_stock_report = StockReport(STOCK_VALIDATION_WORKING_DIR_OLD_SYS, OLD_STOCK_REPORT_FILENAME, SHEET_NAME,
                                   DATETIME_TO_VALIDATE, SELECTED_COL_IDS_OLD_SYS, SELECTED_COL_NAMES)
    df_old_sys = old_stock_report.importExcelSheet()
    new_stock_report = StockReport(STOCK_VALIDATION_WORKING_DIR_NEW_SYS, NEW_STOCK_REPORT_FILENAME, SHEET_NAME,
                                   DATETIME_TO_VALIDATE, SELECTED_COL_IDS_NEW_SYS, SELECTED_COL_NAMES)
    df_new_sys = new_stock_report.importExcelSheet()
    print(f'{name} ended')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run('supermarket report validation')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
