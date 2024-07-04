from django.db import models
from django.contrib.auth.models import User
from .validators import validate_isin


class YieldsFrequencyChoices(models.TextChoices):
    MONTHLY = 12, 'Monthly'
    QUARTERLY = 4, 'Quarterly'
    ANNUALLY = 1, 'Annually'


class Portfolio(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Bond(models.Model):
    emission_name = models.CharField(max_length=50)
    emission_isin = models.CharField(max_length=50, validators=[validate_isin])
    bond_value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    maturity_date = models.DateField(null=True, blank=True)
    yields_frequency = models.IntegerField(
        choices=YieldsFrequencyChoices.choices,
        default=YieldsFrequencyChoices.MONTHLY,
        null=True,
        blank=True
    )
    portfolio = models.ForeignKey(Portfolio, related_name='bonds', on_delete=models.CASCADE)

    def __str__(self):
        return self.emission_name
