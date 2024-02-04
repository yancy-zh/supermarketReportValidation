import math

from pandas import DataFrame

from report import Report


class NewImportPurchaseStockReport(Report):

    def __init__(self, working_dir_name, reportTableName, excel_sheet_name):
        super().__init__(working_dir_name, reportTableName, excel_sheet_name)
        self.SELECTED_COL_NAMES = ['serialNum', 'preSaleCost', 'preSaleAmount', 'preSalePrice', 'importAmount',
                                   'importPrice', 'saleAmount', 'salePrice', 'postSaleAmount', 'postSalePrice']
        self.SELECTED_COL_IDS = r'D, J, M, P, Q, R, T, U, W, X'  # D, J, M, P, Q, R, S, T, V, W # D, J, M, P, Q, R, T, U, W, X

        self.EXCLUDED_SERIAL_NUMS = ['901200', '108800', '901000', '901300', '248084', '240026', '240040', "005080",
                                     "005190", "005020", "005070", "005010", "005140", "005170", "005210", "005100",
                                     "005130", "005120", "005090", "005060", "005030", "005200", "005040", "005110",
                                     "005050", "005160", "005220", "005230", "005250"]
        self.UNITED_SALE = ["004980", "004970", "004910", "004960", "004950", "004940", "004930", "004920", "004400",
                            "004220", "004140", "004150", "003570", "004380", "004240", "004280", "004290", "004340",
                            "006100", "006120", "006130", "006090", "000410", "006020", "000370", "006070", "006060",
                            "006050", "006030", "004740", "004860", "000700", "004890", "000210", "004880", "004870",
                            "004900", "004850", "004810", "004800", "004780", "004770", "004760", "000260", "000220",
                            "000690", "005000", "004990", "000050", "004410", "004420", "004430", "004440", "001070",
                            "004470", "004480", "004490", "000130", "000140", "000170", "000180", "001090", "006110",
                            "000340", "000430", "000460", "000470", "000350", "000480", "006010", "000300", "000290",
                            "000500", "000530", "000270", "000670", "000680", "006080", "004560", "004550", "004540",
                            "000990", "001040", "004520", "004500", "004580", "004600", "004620", "004630", "004650",
                            "004670", "004710", "004720", "000190", "004730", "004450", "004390", "0000400", "003250",
                            "003350", "003340", "001670", "001890", "003260", "0018300", "002910", "001420", "001250",
                            "001940", "001880", "002960", "002980", "001870", "001820", "003330", "003320", "001930",
                            "001860", "001690", "001700", "002970", "001720", "001800", "001790", "001850", "001840",
                            "001660", "001640", "001910", "002930", "003200", "003240", "002890", "001650", "003280",
                            "0016100", "003480", "003490", "003500", "001630", "001330", "001370", "001430", "0013600",
                            "001350", "001340", "001380", "001320", "001300", "001290", "001270", "001260", "001240",
                            "001470", "001180", "001100", "001110", "001130", "001140", "001170", "001410", "001230",
                            "0002920", "001450", "001440", "001540", "001590", "001580", "001570", "001560", "001550",
                            "003510", "002900", "001530", "003520", "003530", "001520", "001500", "001490", "003420",
                            "003360", "001620", "003380", "003390", "003400", "001600", "003460", "003470", "008030",
                            "008100", "008080", "008070", "008060", "008050", "008040", "008110", "008010", "008020",
                            "008120", "008130", "008140", "008150", "008160", "008170", "008180", "008090"]

    def convertTextDataToDigital(self, df):
        for i in [2, 4, 6, 8]:
            df[self.SELECTED_COL_NAMES[i]] = df[self.SELECTED_COL_NAMES[i]].transform(self.floatToInt)
        # for j in [1, 3, 5, 7, 9]:
        #     df[self.SELECTED_COL_NAMES[j]] = df[self.SELECTED_COL_NAMES[j]].transform(self.roundPrice)
        return df

    def removeKeyFromDict(self, dict):
        try:
            del dict['_0']
        except TypeError:
            print(f'dict doesn\'t contain _0')
        except KeyError:
            print(f'dict doesn\'t contain _0')
        try:
            del dict['Unnamed: 0']
            return dict
        except TypeError:
            print(f'dict doesn\'t contain Unnamed: 0')
        except KeyError:
            print(f'dict doesn\'t contain Unnamed: 0')
        return dict

    def cleanTable(self, df, col_idx_serial_no):
        cleaned_df = DataFrame()
        for i in range(len(df)):
            row = df.loc[i, :]
            col_name_serial_num = "serialNum"
            # clean empty row
            try:
                if math.isnan(row[col_name_serial_num]):
                    continue
            except TypeError:
                if self.isSerialNum(row[col_name_serial_num]) \
                        and row[col_name_serial_num] not in self.UNITED_SALE \
                        and len(row[col_name_serial_num]) != 5:
                    # and self.parseAmount(row['preSaleAmount']) != 0
                    # clean united sale
                    cleaned_df = cleaned_df.append(row)
        return cleaned_df
