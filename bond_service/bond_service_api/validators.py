import requests
from django.core.exceptions import ValidationError


def validate_isin(value):
    '''
    Validates the given ISIN (International Securities Identification Number) by querying
    a central depository API.

    Args:
        value (str): The ISIN to validate.

    Returns:
        str: The validated ISIN if found.

    Raises:
        ValidationError: If the ISIN is not found in the central depository or if there's
                         an error in the API request.
    '''
    url = f'https://www.cdcp.cz/isbpublicjson/api/VydaneISINy?isin={value}'
    response = requests.get(url)
    if response.ok:
        data = response.json()
        if not data.get('vydaneisiny'):
            raise ValidationError(f'ISIN {value} is not found in the central depository.')
        else:
            return value
    else:
        raise ValidationError(f'API request error: {response.status_code}')
