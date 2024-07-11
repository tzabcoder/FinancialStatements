# File Imports
import requests
import settings
import pandas as pd
import re

"""
* Financial Statement Reader
*
* Description:
* This class contains the methods to read financial reports filed by
* individual companies to the SEC.
*
* NOTE: This class requires a setting file.
*       The setting file should be named settings.py and contain the following
*       information (as per the SEC API requirements):
*           1. EMAIL = "email name"
*           2. WEBSITE = "website name"
"""
class FinancialStatementReader:
    # SEC URLs
    _CIK_URL = "https://www.sec.gov/files/company_tickers.json"

    # Class Constants
    _10K = '10-K'

    """
    * __init__(): private
    *
    * Creates the header for the SEC API requirements. If the class is constructed
    * with request CIK, the initialization will include requesting all current CIK
    * (Central Index Key) from the SEC.
    *
    * @param[in] request_cik(boolean) - true to request all CIKs listed by the SEC,
    *                                   false otherwise.
    """
    def __init__(self, request_cik=False):
        # Define header for the SEC website request
        self._HEADER = {"User-Agent": f"{settings.WEBSITE} {settings.EMAIL}"}

        # If request CIK flag is true, request all CIKs from SEC
        if request_cik == True:
            self._RequestCIKFromSEC()
        else:
            # Try to read the CIK database
            try:
                self._CIK_DB = pd.read_csv("FS_DataBase\CIK.csv")

            except Exception as e:
                print('SEC CIK database must exist...')

    """
    * _RequestCIKFromSEC(): private
    *
    * Requests all CIKs from the SEC and stores them in a CIK database.
    * The database is also created locally for futher use.
    """
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

    """
    * _GetCIK(): private
    *
    * Gets the CIK corresponding to the provided ticker name. If the CIK exists,
    * it is returned, otherwise -1 is returned indicating the CIK was not found or
    * that the ticker was invalid.
    *
    * @param[in] ticker(str) - ticker to extract the CIK
    * @return CIK if found, otherwise -1
    """
    def _GetCIK(self, ticker):
        cik = -1

        # Loop through all tickers
        if ticker in self._CIK_DB['ticker'].to_list():
            cik = str(self._CIK_DB.loc[(self._CIK_DB['ticker'] == ticker)]['cik_str'][0]) # Get the CIK from the database in string form

            cik = f"{cik:0>10}" # CIKs are 10 digits long and requre leading zeros

        return cik

    """
    * Get10KFilingList(): public
    *
    * Extract the recent 10-K filing information with the associated ticker. The
    * information is stored in a dataframe with the 'primaryDocument' column containing
    * the 10-K file name.
    * If no filing exists, None is returned.
    *
    * @param[in] ticker(str) - ticker name to extract the 10-K filing information
    * @return Dataframe of 10-K filing information, None if DNE.
    """
    def Get10KFilingList(self, ticker):
        filings = None
        cik = self._GetCIK(ticker) # get the CIK associated with the ticker

        # If the CIK is valid
        if cik != -1:
            # Get recent filings with the associated CIK
            filings = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=self._HEADER).json()

            # Extract 10-K filings from rececnt filings
            filings = pd.DataFrame(filings['filings']['recent'])
            filings = filings.loc[filings['primaryDocDescription'] == self._10K]

        return filings

    """
    * Get10KFinancials(): public
    *
    * Request the 10-K filing information given the input parameters.
    *
    * @param[in] acessionNumber(str) - accession number associated with the company
    * @param[in] cik(str)            - CIK associated with the company
    * @param[in] fileName(str)       - 10-K file name associated with the comany
    * @return string of raw text from the filing, None if request error
    """
    def Get10KFinancials(self, accessionNumber, cik, fileName):
        # Construct the filing URL
        filingURL = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accessionNumber}/{fileName}"

        try:
            # Request the filing and extract the raw text
            filing = requests.get(filingURL, headers=self._HEADER)
            filing = filing.text

        except Exception as e:
            filing = None
            print(f'Failed to obtain and parse 10K filing: \n{e}')

        return filing
