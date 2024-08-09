import pandas as pd

class CashflowStatementInterface:
    """ ****************************************************
    * CashflowStatementInterface
    *
    * Description:
    *   The cash flow statement interface will take the CF statement
    *   and export it to an Excel file (.xslx).
    **************************************************** """

    _CASHFLOW_STATEMENT_DIR = "financials\\cashflow_statement\\"

    def __init__(self, symbol: str, cashflowStatement: pd.DataFrame) -> None:
        """ ****************************************************
        * __init__()
        *
        * Description:
        *   Verifies that the CF statement is the correct type, and
        *   writes the data to the financials (cashflow) database.
        *
        * symbol -> str                     : String symbol of the ticket
        * cashflowStatement -> pd.DataFrame : CF statement dataframe
        **************************************************** """

        if type(cashflowStatement) == pd.DataFrame:
            self._ExportToExcel(symbol, cashflowStatement)

        else:
            print(f"{self.__init__.__name__}(): Cashflow statement must be in the form of pd.DataFrame...")

    def _ExportToExcel(self, symbol: str, cashflowStatement: pd.DataFrame) -> None:
        """ ****************************************************
        * _ExportToExcel()
        *
        * Description:
        *   Write the cashflow statement to the Excel file.
        *
        * symbol -> str                     : String symbol of the ticket
        * cashflowStatement -> pd.DataFrame : CF statement dataframe
        **************************************************** """

        filename = f"{symbol}_cashflowStatement.xlsx"

        try:
            cashflowStatement.to_excel(self._CASHFLOW_STATEMENT_DIR + filename)

        except Exception as e:
            print(f"{self._ExportToExcel.__name__}(): Could not write cashflow statement to {filename}...\n{e}")