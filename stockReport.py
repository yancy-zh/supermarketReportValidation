import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
from numpy import NaN
import math
import re
import csv
import os
import xlrd
import string


class StockReport:

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name, dateTime, excel_selected_column_ids,
                 excel_selected_column_names):
        self.metadata_filename = os.path.join(working_dir_name, reportTableName)
        self.excel_sheet_name = excel_sheet_name
        self.dateTime = dateTime
        self.excel_selected_column_ids = excel_selected_column_ids
        self.excel_selected_column_names = excel_selected_column_names

    def importExcelSheet(self):
        if not os.path.isfile(self.metadata_filename):
            print(f"file {self.metadata_filename} doesn't exists")
            return
        dict_metadata = pd.read_excel(self.metadata_filename, header=None, skiprows=[0],
                                      usecols=self.excel_selected_column_ids,
                                      names=self.excel_selected_column_names
                                      ).to_dict(orient='list')
        return dict_metadata
