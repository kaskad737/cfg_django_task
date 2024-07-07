from .models import Portfolio, Bond
from django.db.models.query import QuerySet
from typing import Dict
from django.utils import timezone
from .serializers import BondSerializer
from decimal import Decimal


def get_portfolio_analysis(portfolio: Portfolio) -> Dict:
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
