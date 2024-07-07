from .models import Portfolio, Bond
from django.db.models.query import QuerySet
from typing import Dict
from django.utils import timezone
from .serializers import BondSerializer
from decimal import Decimal


def get_portfolio_analysis(portfolio: Portfolio) -> Dict:
    '''
    Analyzes the bonds within a portfolio and returns a dictionary containing
    various metrics and details about the portfolio's bond holdings.

    Args:
        portfolio (Portfolio): The portfolio object containing bonds to be analyzed.

    Returns:
        Dict: A dictionary with the following keys:
            - 'average_interest_rate' (Decimal): The average interest rate of all bonds in the portfolio.
            - 'nearest_maturity_bond' (dict): Serialized data of the bond with the nearest maturity date.
            - 'total_value' (Decimal): The total value of all bonds in the portfolio.
            - 'future_value' (Decimal): The future value of the portfolio, calculated based on the average interest rate
              and the time until the nearest maturity date.
            If the portfolio contains no bonds, returns a dictionary with a single key:
            - 'message' (str): A message indicating that the portfolio contains no bonds.

    Raises:
        This function does not raise any exceptions.

    Note:
        The 'nearest_maturity_bond' is determined based on the maturity date closest to the current date.
        The future value is calculated assuming compound interest over the time until the nearest maturity date.
    '''
    all_portfolio_bonds: QuerySet[Bond] = portfolio.bonds.all()
    if all_portfolio_bonds.exists():
        total_value = Decimal(sum(all_portfolio_bonds.values_list('bond_value', flat=True)))
        avg_interest_rate = Decimal(sum(all_portfolio_bonds.values_list(
            'interest_rate', flat=True)) / all_portfolio_bonds.count())
        nearest_maturity_bond: Bond = min(all_portfolio_bonds, key=lambda bond: bond.maturity_date)
        years = Decimal((nearest_maturity_bond.maturity_date - timezone.now().date()).days / Decimal(365.25))

        future_value = total_value * (1 + avg_interest_rate / 100) ** years
        return {
            'average_interest_rate': avg_interest_rate,
            'nearest_maturity_bond': BondSerializer(nearest_maturity_bond).data,
            'total_value': total_value,
            'future_value': future_value,
        }
    else:
        return {'message': 'Portfolio contains no bonds.'}
