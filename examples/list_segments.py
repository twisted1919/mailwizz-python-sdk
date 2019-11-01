from setup_api import setup
from mailwizz.endpoint.list_segments import ListSegments

"""
SETUP THE API
"""
setup()

"""
CREATE THE ENDPOINT
"""
endpoint = ListSegments()


"""
GET ALL SEGMENTS OF A LIST
"""
response = endpoint.get_segments(list_uid='LIST_UID')

"""
DISPLAY RESPONSE
"""
print(response.content)
