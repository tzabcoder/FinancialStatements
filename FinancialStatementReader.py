import requests
import settings
import pandas as pd
import re

class FinancialStatementReader:
    # SEC URLs
    _CIK_URL = "https://www.sec.gov/files/company_tickers.json"

    # Class Constants
    _10K = '10-K'

    def __init__(self, request_cik=False):
        # Define header for the SEC website request
        self._HEADER = {"User-Agent": f"{settings.WEBSITE} {settings.EMAIL}"}

        # If request CIK flag is true, request all CIKs from SEC
        if request_cik == True:
            self._RequestCIKFromSEC()
        else:
            self._CIK_DB = pd.read_csv("FS_DataBase\CIK.csv")

    def _RequestCIKFromSEC(self):
        # Centeral Index Key (CIK)
        # SEC assigns a CIK for each company (which is used in the document requests)
        symbolToCIK = requests.get(CIK_URL, headers=self._HEADER).json()

        centralIndexId = pd.DataFrame(symbolToCIK)
        centralIndexId = centralIndexId.transpose()
        centralIndexId.set_index('ticker', inplace=True)

        # Write the CIK database to file
        centralIndexId.to_csv('FS_Database/CIK.csv')

        self._CIK_DB = centralIndexId

    def _GetCIK(self, ticker):
        cik = -1

        if ticker in self._CIK_DB['ticker'].to_list():
            cik = str(self._CIK_DB.loc[(self._CIK_DB['ticker'] == ticker)]['cik_str'][0]) # Get the CIK from the database in string form

            cik = f"{cik:0>10}" # CIKs are 10 digits long and requre leading zeros

        return cik

    def Get10KFilingList(self, ticker):
        filings = None
        cik = self._GetCIK(ticker)

        # If the CIK is valid
        if cik != -1:
            filings = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=self._HEADER).json()

            # Extract 10-K filings
            filings = pd.DataFrame(filings['filings']['recent'])
            filings = filings.loc[filings['primaryDocDescription'] == self._10K]

        return filings

    def Get10KFinancials(self, accessionNumber, cik, fileName):
        filingURL = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accessionNumber}/{fileName}"

        try:
            filing = requests.get(filingURL, headers=self._HEADER)
            filing = filing.text

        except Exception as e:
            filing = None
            print(f'Failed to obtain and parse 10K filing: \n{e}')

        return filing