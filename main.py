# coding=utf-8
from  validateReports import ValidateReports





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    validateReports = ValidateReports()
    # validateReports.validateStockReports('比对库存表')
    # validateReports.validateSaleReports('比对销售表')
    # validateReports.validateTransactionReports('比对流水表')
    # validateReports.validateSaleByCategory('比对按品类分类汇总销售表')
    # validateReports.compareTransactionReports('比对流水表按商品汇总')
    validateReports.validatePurchaseSaleStockReports('比对进销存表')
