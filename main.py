# coding=utf-8
from validateReports import ValidateReports

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    validateReports = ValidateReports()
    # validateReports.validateStockReports('比对库存表')
    # validateReports.validateSaleReports('比对销售表')
    validateReports.validateTransactionReports('比对流水表')
    # validateReports.compareTransactionReports('比对流水表按商品汇总')
    # validateReports.validateSaleByCategory('比对按品类分类汇总销售表')
    # validateReports.validatePurchaseSaleStockReports('进销存表')
    # validateReports.validateImportReports('比对入库单')
    # validateReports.validateImportPurchaseStockGroupBySupplier('进销存变动表')
    # validateReports.validateInventoryCountingReports('盘点差异表')
    # validateReports.validateInventoryReports('商品一览表')
    # validateReports.cleanUpReport('报表数据筛选')
    # validateReports.checkStockAndImportPurchase('库存表与进销存表的库存数量')
