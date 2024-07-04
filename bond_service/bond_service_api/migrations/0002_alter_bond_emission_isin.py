# Generated by Django 4.0.6 on 2024-07-04 08:08

import bond_service_api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond_service_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bond',
            name='emission_isin',
            field=models.CharField(max_length=50, validators=[bond_service_api.validators.validate_isin]),
        ),
    ]