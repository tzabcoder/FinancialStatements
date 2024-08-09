import pandas as pd

class BalanceSheetInterface:
    """ ****************************************************
    * BalanceSheetInterface
    *
    * Description:
    *   The balance sheet interface will take the balance sheet
    *   and export it to an Excel file (.xslx).
    **************************************************** """

    _BALANCE_SHEET_DIR = "financials\\balance_sheet\\"

    def __init__(self, symbol: str, balancesheet: pd.DataFrame) -> None:
        """ ****************************************************
        * __init__()
        *
        * Description:
        *   Verifies that the balancesheet is the correct type, and
        *   writes the data to the financials (balancesheet) database.
        *
        * symbol -> str                : String symbol of the ticket
        * balancesheet -> pd.DataFrame : Balance sheet dataframe
        **************************************************** """

        if type(balancesheet) == pd.DataFrame:
            self._ExportToExcel(symbol, balancesheet)

        else:
            print(f"{self.__init__.__name__}(): Balancesheet must be in form of pd.DataFrame...")

    def _ExportToExcel(self, symbol: str, balancesheet: pd.DataFrame) -> None:
        """ ****************************************************
        * _ExportToExcel()
        *
        * Description:
        *   Write the balancesheet to the Excel file.
        *
        * symbol -> str                : String symbol of the ticket
        * balancesheet -> pd.DataFrame : Balance sheet dataframe
        **************************************************** """

        filename = f"{symbol}_balancesheet.xlsx"

        try:
            balancesheet.to_excel(self._BALANCE_SHEET_DIR + filename)

        except Exception as e:
            print(f"{self._ExportToExcel.__name__}(): Could not write balance sheet to {filename}...\n{e}")

