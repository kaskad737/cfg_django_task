from django.db import models
from django.contrib.auth.models import User
from .validators import validate_isin


class YieldsFrequencyChoices(models.TextChoices):
    '''
    YieldsFrequencyChoices: A Django enumeration for yield frequency options.

    This class defines the frequency choices for yields as a set of predefined constants.

    Attributes:
        MONTHLY (int, str): Represents monthly yield frequency with a value of 12.
        QUARTERLY (int, str): Represents quarterly yield frequency with a value of 4.
        ANNUALLY (int, str): Represents annual yield frequency with a value of 1.
    '''
    MONTHLY = 12, 'Monthly'
    QUARTERLY = 4, 'Quarterly'
    ANNUALLY = 1, 'Annually'


class Portfolio(models.Model):
    '''
    Portfolio: A Django model representing a portfolio.

    Attributes:
        name (CharField): The name of the portfolio. Must be unique and cannot be null or blank.
                          Maximum length is 255 characters.
        created_by (ForeignKey): A foreign key reference to the User who created the portfolio.
                                 If the referenced User is deleted, the portfolio will also be deleted.
        created_at (DateField): The date the portfolio was created.
        updated_at (DateField): The date the portfolio was updated.

    Methods:
        __str__(): Returns the name of the portfolio as a string representation.
    '''
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Bond(models.Model):
    '''
     Model representing a bond.

    Attributes:
    ----------
    emission_name : str
        The name of the bond emission (unique).
    emission_isin : str
        The ISIN code of the bond emission (unique). Validated by the `validate_isin` function.
    bond_value : Decimal
        The value of the bond.
    interest_rate : Decimal
        The interest rate of the bond.
    purchase_date : date
        The date the bond was purchased.
    maturity_date : date
        The date the bond matures.
    yields_frequency : int
        The frequency of yield payments, defined by `YieldsFrequencyChoices`.
    portfolio : ForeignKey
        The portfolio to which this bond belongs, with a cascade delete behavior.
    created_at : date
        The date the bond record was created.
    updated_at : date
        The date the bond record was updated.

    Methods:
    -------
    __str__():
        Returns the emission name of the bond.
    '''
    emission_name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    emission_isin = models.CharField(max_length=50, unique=True, validators=[validate_isin], null=False, blank=False)
    bond_value = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    purchase_date = models.DateField(null=False, blank=False)
    maturity_date = models.DateField(null=False, blank=False)
    yields_frequency = models.IntegerField(
        choices=YieldsFrequencyChoices.choices,
        default=YieldsFrequencyChoices.MONTHLY,
        null=False,
        blank=False
    )
    portfolio = models.ForeignKey(Portfolio, related_name='bonds', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.emission_name
