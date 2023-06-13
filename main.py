# coding=utf-8
from  validateReports import ValidateReports





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    validateReports = ValidateReports()
    # validateReports.validateStockReports('比对库存表')
    validateReports.validateSaleReports('比对销售表')
