import pandas as pd
import os
import re
class OldTransactionRecordReport:
    _SELECTED_COL_NAMES_OLD_SYS = ['transactionNo', 'transactionType', 'productId', 'amount', 'price', 'sum']
    _SELECTED_COL_IDS_OLD_SYS = r'C, D, F, H, I, J'
    _AMOUNT_PATTERN = re.compile(r'-?\d*\,?\d+\.?\d?\d?')

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        self.metadata_filename = os.path.join(working_dir_name, reportTableName)
        self.excel_sheet_name = excel_sheet_name

    def importExcelSheet(self):
        if not os.path.isfile(self.metadata_filename):
            print(f"file {self.metadata_filename} doesn't exists")
            return
        df_metadata = pd.read_excel(self.metadata_filename, header=None, skiprows=[0],
                                    usecols=self._SELECTED_COL_IDS_OLD_SYS,
                                    names=self._SELECTED_COL_NAMES_OLD_SYS
                                    )
        return df_metadata

    def getTransactionNum(self, df, ind):
        return df[self._SELECTED_COL_NAMES_OLD_SYS[0]][ind]

    def getSelectedTransaction(self, df, transactionNum):
        row_filtered = df[df[self._SELECTED_COL_NAMES_OLD_SYS[0]]== transactionNum].values.toList()
        return row_filtered
