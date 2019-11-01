from setup_api import setup
from mailwizz.endpoint.countries import Countries

"""
SETUP THE API
"""
setup()

"""
CREATE THE ENDPOINT
"""
endpoint = Countries()

"""
GET ALL ITEMS
"""
response = endpoint.get_countries(page=1, per_page=10)

"""
DISPLAY RESPONSE
"""
print(response.content)

"""
GET COUNTRY ZONES
"""
response = endpoint.get_zones(country_id=223, page=1, per_page=10)

"""
DISPLAY RESPONSE
"""
print(response.content)
