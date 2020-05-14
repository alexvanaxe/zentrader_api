"""
Contains a variety of performance reports and information
"""
from sell.models import SellData
from datetime import datetime, timedelta


class Report():
    """
    Class containing some reports.
    """
    def total_profit(self):
        """
        Returns the profit of all completed operations.
        """
        sells = SellData.executions.all()
        total = 0
        for sell in sells:
            total += sell.profit()

        return total

    def total_monthly_profit(self):
        """
        Returns a list of the profit by month
        """
        refdt = datetime.now()
        ltdate = datetime(refdt.year - 1, refdt.month, refdt.day)

        one_year_sells = SellData.executions.filter(execution_date__lte=refdt,
                                                    execution_date__gte=ltdate)

        monthly_profit = {}

        for month in range(1, 13):
            monthly_profit.update({month: 0})

        for sell in one_year_sells:
            monthly_profit[sell.execution_date.month] = \
                           monthly_profit[sell.execution_date.month] + \
                           sell.profit()

        return monthly_profit
