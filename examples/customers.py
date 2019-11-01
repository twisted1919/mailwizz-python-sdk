from setup_api import setup
from mailwizz.endpoint.customers import Customers

"""
SETUP THE API
"""
setup()

"""
CREATE THE ENDPOINT
"""
endpoint = Customers()

"""
CREATE CUSTOMER
"""
response = endpoint.create({
    'customer': {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@doe.com',
        'password': 'superDuperPassword',
        'timezone': 'UTC',
        'birthDate': '1979-07-30'
    },
    # company is optional, unless required from app settings
    'company': {
        'name': 'John Doe LLC',
        'country': 'United States',  # see the countries endpoint for available countries and their zones
        'zone': 'New York',  # see the countries endpoint for available countries and their zones
        'city': 'Brooklyn',
        'zip_code': 11222,
        'address_1': 'Some Address',
        'address_2': 'Some Other Address',
    },
})

"""
DISPLAY RESPONSE
"""
print(response.content)
