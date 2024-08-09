import pandas as pd

class IncomeStatementInterface:
    """ ****************************************************
    * IncomeStatementInterface
    *
    * Description:
    *   The income statement interface will take the income statement
    *   and export it to an Excel file (.xslx).
    **************************************************** """

    _INCOME_STATEMENT_DIR = "financials\\income_statement\\"

    def __init__(self, symbol: str, incomeStatement: pd.DataFrame) -> None:
        """ ****************************************************
        * __init__()
        *
        * Description:
        *   Verifies that the CF statement is the correct type, and
        *   writes the data to the financials (cashflow) database.
        *
        * symbol -> str                    : String symbol of the ticket
        * incomeStatement -> pd.DataFrame : income statement dataframe
        **************************************************** """

        if type(incomeStatement) == pd.DataFrame:
            self._ExportToExcel(symbol, incomeStatement)

        else:
            print(f"{self.__init__.__name__}(): Income statement must be in the form of pd.DataFrame...")

    def _ExportToExcel(self, symbol: str, incomeStatement: pd.DataFrame) -> None:
        """ ****************************************************
        * _ExportToExcel()
        *
        * Description:
        *   Write the cashflow statement to the Excel file.
        *
        * symbol -> str                    : String symbol of the ticket
        * incomeStatement -> pd.DataFrame : income statement dataframe
        **************************************************** """

        filename = f"{symbol}_incomeStatement.xlsx"

        try:
            incomeStatement.to_excel(self._INCOME_STATEMENT_DIR + filename)

        except Exception as e:
            print(f"{self._ExportToExcel.__name__}(): Could not write income statement to {filename}...\n{e}")