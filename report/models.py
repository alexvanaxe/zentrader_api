"""
Contains a variety of performance reports and information
"""
from sell.models import SellData


class Report():
    """
    Class containing some reports.
    """
    def totalProfit(self):
        """
        Returns the profit of all completed operations.
        """
        sells = SellData.executions.all()
        total = 0
        for sell in sells:
            total += sell.profit()

        return total
