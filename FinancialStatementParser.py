import time
import warnings
import pandas as pd
import FinancialStatementReader as fsr
from bs4 import BeautifulSoup

# File Settings
warnings.filterwarnings('ignore')

class FinancialStatementParser:
    def __init__(self, request_cik=False):
        # Create the statement reader
        self._financialStatementReader = fsr.FinancialStatementReader(request_cik)

    def _ReconstructFinancials(self, financials, idx):
        # Convert the financials into a BeautifulSoup object
        financialsContent = BeautifulSoup(financials, 'html')

        # TEST => write to file for visual inpection
        html = financialsContent.prettify('utf-8')
        filename = f'inspection_{idx}.html'
        with open(filename, 'wb') as file:
            file.write(html)

        # 1. Find the table under question
        # 2. Convert the table to a dataframe

        # Reconstruct the balance sheet
        # Reconstruct the income statement
        # Reconstruct the statement of cash flows

    def ParseStatements(self, ticker):
        _10K_filings = self._financialStatementReader.Get10KFilingList(ticker)

        cik = str(_10K_filings['accessionNumber'].iloc[0]).split('-')[0]

        for idx in range(len(_10K_filings)):
            accessionNumber = str(_10K_filings['accessionNumber'].iloc[idx])
            fileName = str(_10K_filings['primaryDocument'].iloc[idx])
            accessionNumber = accessionNumber.split('-')
            accessionNumber = accessionNumber[0] + accessionNumber[1] + accessionNumber[2]

            filing10K = self._financialStatementReader.Get10KFinancials(accessionNumber, cik, fileName)

            if filing10K is not None:
                financials = self._ReconstructFinancials(filing10K, idx)
            else:
                print(f'Could not obtain financials for: {fileName}')

            time.sleep(1)


# Example of usage
statementParser = FinancialStatementParser()
statementParser.ParseStatements('AAPL')