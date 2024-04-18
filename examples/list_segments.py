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

"""
GET ONE ITEM
"""
response = endpoint.get_segment(list_uid='LIST_UID', segment_uid='SEGMENT_UID')

"""
DISPLAY RESPONSE
"""
print(response.content)

"""
GET ALL SUBSCRIBERS OF A LIST SEGMENT
"""
response = endpoint.get_subscribers(list_uid='LIST_UID', segment_uid='SEGMENT_UID', page=1, per_page=10)

"""
DISPLAY RESPONSE
"""
print(response.content)