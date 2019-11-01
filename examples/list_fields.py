from setup_api import setup
from mailwizz.endpoint.list_fields import ListFields

"""
SETUP THE API
"""
setup()

"""
CREATE THE ENDPOINT
"""
endpoint = ListFields()


"""
GET ALL FIELDS OF A LIST
"""
response = endpoint.get_fields(list_uid='LIST_UID')

"""
DISPLAY RESPONSE
"""
print(response.content)
