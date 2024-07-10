import time
import re
import warnings
import pandas as pd
import FinancialStatementReader as fsr
from bs4 import BeautifulSoup

# File Settings
warnings.filterwarnings('ignore')

"""
* Financial Statement Parser
*
* Description:
* This class contains the methods to parse 10-K and 10-Q finacial statements.
* In particular, this class reconstructs the financials from the SEC filings.
"""
class FinancialStatementParser:
    # Table headers (titles)
    _TBL_HDRS = [
        "CONSOLIDATED STATEMENTS OF OPERATIONS",
        "CONSOLIDATED BALANCE SHEETS",
        "CONSOLIDATED STATEMENTS OF COMPREHENSIVE INCOME",
        "CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY",
        "CONSOLIDATED STATEMENTS OF CASH FLOWS",
    ]

    # List of months in string format
    _MONTHS = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]

    # List of number characters that can exist in the financial statement tables
    _NUMBER_CHARACTERS = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ',', '(', ')', '.', '-'
    ]

    """
    * __init__(): private
    *
    * Initializes the parser instance by creating the financial statement interface.
    * (FinancialStatementReader)
    * If the input CIK request parameter is true, then the reader interface will be
    * created with the true flag.
    *
    * @param[in] request_cik(boolean) - true to request all CIKs listed by the SEC,
    *                                   false otherwise.
    """
    def __init__(self, request_cik=False):
        # Create the statement reader
        self._financialStatementReader = fsr.FinancialStatementReader(request_cik)

    """
    * _HasMonth(): private
    *
    * Checks if a given string item contains a month.
    *
    * @param[in] item(string) - string to check
    * @returns true if has a month, flase otherwise
    """
    def _HasMonth(self, item):
        hasDate = False

        # Check for all months
        for month in self._MONTHS:
            if month in item:
                hasDate = True

        return hasDate

    """
    * _HasNumberCharacters(): private
    *
    * Checks if a given string item contains a specific number characters.
    *
    * @param[in] item(string) - string to check
    * @returns true if has a number characters, flase otherwise
    """
    def _HasNumberCharacters(self, item):
        hasNumbers = True

        # Check all characters in the string
        for char in item:
            # Set the flag if an invalid number charcter
            if char not in self._NUMBER_CHARACTERS:
                hasNumbers = False

        return hasNumbers

    """
    * _ParseNumberItem(): private
    *
    * Converts a number item into either an integer or float.
    * 1,234 OR 123                   => converted into positive integers
    * (1,234) OR (123) OR -123       => converted into negative integers
    * 1,234.1 OR 123,4               => converted into positive floats
    * (1,234.1) OR (123.1) OR -123.4 => converted into negative floats
    *
    * @param[in] number(string) - string number to convert into a number
    * @returns t_num
    """
    def _ParseNumberItem(self, number):
        t_num = number

        # Handle positive integers
        if (',' in number or ',' not in number) and \
           ('(' not in number and ')' not in number and '-' not in number) and \
            ('.' not in number):

            t_num = number.replace(",", "")

            t_num = int(t_num)

        # Handle negative integers
        if (',' in number or ',' not in number) and \
           (('(' in number and ')' in number) or ('-' in number)) and \
           ('.' not in number):

           t_num = number.replace(",", "")
           t_num = t_num.replace("(", "")
           t_num = t_num.replace(")", "")
           t_num = t_num.replace("-", "")

           t_num = int(t_num) * -1

        # Handle positive decimals
        if (',' in number or ',' not in number) and \
           ('(' not in number and ')' not in number and '-' not in number) and \
           ('.' in number):

            t_num = number.replace(",", "")

            t_num = float(t_num)

        # Handle negative decimals
        if (',' in number or ',' not in number) and \
           (('(' in number and ')' in number) or ('-' in number)) and \
           ('.' in number):

           t_num = number.replace(",", "")
           t_num = t_num.replace("(", "")
           t_num = t_num.replace(")", "")
           t_num = t_num.replace("-", "")

           t_num = float(t_num) * -1

        return t_num

    """
    * _ProcessRow(): private
    *
    * Format a given row(list) that was extracted from the raw SEC filing.
    * All blank items '' and $ will be removed for formating.
    *
    * @param[in] row(list) - row to format
    * @returns t_row
    """
    def _ProcessRow(self, row):
        t_row = []

        # Process all items in the row
        for item in row:
            if item != '' and item != '$':
                # Process date items
                if self._HasMonth(item):
                    if 'Date' not in t_row:
                        t_row.append('Date')

                    t_row.append(item)

                # Process number items
                elif self._HasNumberCharacters(item):
                    t_row.append(self._ParseNumberItem(item))

                # Process string items
                else:
                    t_row.append(item)

        return t_row # formatted row

    """
    * _ExtractTable(): private
    *
    * Extract all financial statement tables from the given SEC filing.
    *
    * @param[in] financials(str) - financial document in string format
    * @param[in] tableHeader(str) - name of the table in string format
    * @return financials_df (dataframe of the finacial tables)
    """
    def _ExtractTable(self, financials, tableHeader):
        # Convert the financials into a BeautifulSoup object and find table header
        financialsContent = BeautifulSoup(financials, 'html')
        bs = financialsContent.find_all(text=re.compile(tableHeader))

        table = []
        for nextItem in bs:
            # find all table items in the BS object
            for row in nextItem.find_next("table").find_all("tr"):
                t = [cell.get_text(strip=True) for cell in row.find_all("td")] # extract the table row
                t = self._ProcessRow(t)                                        # process/format the table row

                # Omit empty table rows
                if len(t) != 0:
                    table.append(t)

        # Dataframe construction
        financials_df = pd.DataFrame(table)
        colLen = len(financials_df.columns)

        # Rename the colukmns to temporary values
        colNames = []
        colName = 'col_'
        for i in range(colLen):
            if i > 0:
                c_name = colName + str(i)
                colNames.append(c_name)
            else:
                colNames.append('Category')

        financials_df.columns = colNames
        financials_df.set_index(colNames[0], inplace=True)

        # Rename the columns to the date values
        dates = financials_df.loc['Date']
        colDates = [date for date in dates]

        financials_df.columns = colDates
        financials_df.drop('Date', axis=0, inplace=True)

        return financials_df

    """
    * _ReconstructFinancials(): private
    *
    * Reconstructs all financial statement tables from the SEC filing.
    * For the list of table names, see @_TBL_HDRS.
    *
    * @param[in] financials(str) - financial document in string format
    * @return financialTables (dict of financial tables)
    """
    def _ReconstructFinancials(self, financials):
        # Dict keys are the table headers (names)
        financialTables = {}

        for hdr in self._TBL_HDRS:
            financialTables[hdr] = self._ExtractTable(financials, hdr)

        return financialTables

    """
    * Extract10KFinancialStatementTables(): public
    *
    * Extract the 10-K financial data tables from the SEC filing. The filings
    * are all recent (historical) filings provided by the SEC.
    * Requests the information, and calls the required parsing functions.
    *
    * @param[in] ticker(str) - ticker to extract financial data
    * @return historicalFilings (list of dicts for all historical filings)
    """
    def Extract10KFinancialStatementTables(self, ticker):
        _10K_filings = self._financialStatementReader.Get10KFilingList(ticker)

        cik = str(_10K_filings['accessionNumber'].iloc[0]).split('-')[0]

        historicalFilings = []
        for idx in range(len(_10K_filings)):
            # Extract the acession number and file name => for SEC request
            accessionNumber = str(_10K_filings['accessionNumber'].iloc[idx])
            fileName = str(_10K_filings['primaryDocument'].iloc[idx])
            accessionNumber = accessionNumber.split('-')
            accessionNumber = accessionNumber[0] + accessionNumber[1] + accessionNumber[2]

            # Get the 10-K filing
            filing10K = self._financialStatementReader.Get10KFinancials(accessionNumber, cik, fileName)

            # Only process the filing if it exists
            if filing10K is not None:
                financials = self._ReconstructFinancials(filing10K)
            else:
                financials = None
                print(f'Could not obtain financials for: {fileName}')

            historicalFilings.append(financials)

            time.sleep(1)

        return historicalFilings


# Example of usage TEST
statementParser = FinancialStatementParser()
tables = statementParser.Extract10KFinancialStatementTables('AAPL')

print(tables)
