# coding=utf-8
from validateReports import ValidateReports

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    validateReports = ValidateReports()
    # validateReports.validateStockReports('比对库存表')
    # validateReports.validateStockReportsNewVsNew('比对不同日期新系统库存表')
    # validateReports.validateSaleReports('比对表7销售汇总明细表')
    # validateReports.validateSaleReports2('比对表7销售汇总明细表仅小计数量和小计金额')
    # validateReports.validateTransactionReports('预处理表9流水表')
    validateReports.compareTransactionReports('预处理表9流水表')  # 请不要修改参数
    # validateReports.validateSaleByCategory('比对按品类分类汇总销售表')
    # validateReports.validateSaleBySupplier('比对按供应商分类汇总销售表')
    # validateReports.validatePurchaseSaleStockReports('进销存汇总明细表')
    # validateReports.validateImportPurchaseStockGroupBySupplier('进销存变动表')
    # validateReports.validateImportReports('比对入库单')
    # validateReports.validateImportReportsBySupplier('比对表14入库汇总-按供应商')
    # validateReports.validateImportInvoice('比对入库单据')
    # validateReports.validateInventoryCountingReports('盘点差异表')
    # validateReports.cleanUpReport('报表数据筛选')
    # validateReports.checkStockAndImportPurchase('库存表与进销存表的库存数量')
    # validateReports.validateBasicInfoReports('商品一览表')
    # validateReports.validateSaleAndImportPurchaseStock('销售表与进销存表的销售数量及金额')
    # validateReports.validateSaleAndExport('销售表与出库汇总明细表的出库数量及金额')
    # validateReports.validateExportReportsBySupplier('新旧系统出库汇总按供应商品类排序')
    # validateReports.validateExportReports('新旧系统出库汇总明细表')
    # validateReports.validateExportReportBySupplier('出库汇总新系统按供应商出表')
    # validateReports.mergeBasicInfoAndStock("旧系统基本信息和库存表合并")
