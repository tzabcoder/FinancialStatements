import pandas as pd

class EnterpriseValue:
    # Asset Inputs
    _totalNonOperatingAssets = 0

    # Liability Inputs
    _totalLiabilities = 0

    # Enterprise Value Variables
    enterpriseValue = 0             # Enterprise value (either on a total or per-share basis)
    enterpriseValuePerShare = False # Flag to indicate if the eterprise value is on a per share basis

    def __init__(self, fcf: list, discountRate: float, midyearFactor: float = 1.0) -> None:
        """ ****************************************************
        * __init__()
        *
        * Description:
        *   Creates the initial DataFrame of future free-cash-flows (FFCF) and
        *   the corresponding look-forward year.
        *
        * fcf -> list[float] : future free-cash-flows
        * discountRate -> float : the current weighted average cost of capital (WACC)
        * midyearFactor -> float : mid-year adjustment factor for the PV(CF)
        **************************************************** """

        self._freeCashFlows = fcf
        self._discountRate = discountRate
        self._midyearAdjFactor = midyearFactor

        forwardYear = [i+1 for i in range(len(fcf))]

        self._cashFlowDF = pd.DataFrame(self._freeCashFlows, columns=['FCF'])
        self._cashFlowDF['Year'] = forwardYear

    def addNonOperatingAssets(self, assets: list) -> None:
        """ ****************************************************
        * addNonOperatingAssets()
        *
        * Description:
        *   Adds the total value of the non-operating assets together. These
        *   assets are not included in FCF. Summing the values yields the
        *   total non-operating asset value.
        *
        * assets -> list[float] : list of all non-operating asset values
        **************************************************** """

        for asset in assets:
            self._totalNonOperatingAssets += asset

    def addLiabilities(self, liabilities: list) -> None:
        """ ****************************************************
        * addLiabilities()
        *
        * Description:
        *   Adds the total value of the outstanding liabilities (claims)
        *   against the enterprise value of the company.
        *
        * liabilities -> list[float] : list of all non-equity claims against
        *                              the enterprise value
        **************************************************** """

        for liability in liabilities:
            self._totalLiabilities += liability

    def calculateEnterpriseValue(self, sharesOutstanding: int = -1) -> (float, bool):
        """ ****************************************************
        * calculateEnterpriseValue()
        *
        * Description:
        *   Calculates the enterprise value of the cash flows. If a total number of
        *   shares outstanding are provided, the function will calculate EV on a
        *   per-share basis. Otherwise, the EV will be the cash flow's equity value.
        *
        *   NOTE: The total shares outstanding input must match the unites of the CFs.
        *         (i.e. if the CFs are in $ millions, the # of shares must be in millions)
        *
        * sharesOutstanding -> int (default=-1) : total number of shares outstanding
        * returns (float, bool) : The enterprise value and flag indicating if it is on a
        *                         per-share basis
        **************************************************** """

        # Calculate the discount factor (setting the terminal value)
        self._cashFlowDF['Discount_Factor'] = 1 / (1 + self._discountRate) ** self._cashFlowDF['Year']
        self._cashFlowDF['Discount_Factor'].at[len(self._cashFlowDF)-1] = self._cashFlowDF['Discount_Factor'][len(self._cashFlowDF)-2]

        # Calculate the PR of the future free-cash-flows
        self._cashFlowDF['PV_FCF'] = self._cashFlowDF['FCF'] * self._cashFlowDF['Discount_Factor']

        pvCF = self._cashFlowDF['PV_FCF'].sum()

        valueOperations = pvCF * self._midyearAdjFactor
        enterpriseValue = valueOperations + self._totalNonOperatingAssets
        equityValue = enterpriseValue + self._totalLiabilities

        # Determine whether to calculate EV on a per-share basis
        if sharesOutstanding > 0:
            equityValue = equityValue / sharesOutstanding
            self.enterpriseValuePerShare = True
        else:
            self.enterpriseValuePerShare = False

        # Set the enterprise value
        self.enterpriseValue = equityValue

        return self.enterpriseValue, self.enterpriseValuePerShare

# TEST CODE ---------------------
fcf = [3472,4108,4507,4892,5339,5748,6194,6678,7086,7523,168231]
dr = 0.08
adjFactor = 1.039

ev = EnterpriseValue(fcf, dr, adjFactor)

assets = [4136,148]
liabilities = [-10872,-5042,-5841,-14]

ev.addNonOperatingAssets(assets)
ev.addLiabilities(liabilities)

enterpriseVal, perShare = ev.calculateEnterpriseValue(sharesOutstanding=923)

print(enterpriseVal)