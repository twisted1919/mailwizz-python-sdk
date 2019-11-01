from setup_api import setup
from mailwizz.endpoint.list_subscribers import ListSubscribers

"""
SETUP THE API
"""
setup()

"""
CREATE THE ENDPOINT
"""
endpoint = ListSubscribers()


"""
GET ALL SUBSCRIBERS OF A LIST
"""
response = endpoint.get_subscribers(list_uid='LIST_UID', page=1, per_page=10)

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
GET ONE SUBSCRIBER FROM A LIST
"""
response = endpoint.get_subscriber(list_uid='LIST_UID', subscriber_uid='SUBSCRIBER_UID')

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
SEARCH BY EMAIL
"""
response = endpoint.email_search(list_uid='LIST_UID', email_address='john.doe@example.com')

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
SEARCH BY EMAIL IN ALL LISTS
"""
response = endpoint.email_search_all_lists(email_address='john.doe@example.com')

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
SEARCH BY CUSTOM FIELDS IN A LIST
"""
response = endpoint.search_by_custom_fields(list_uid='LIST_UID', fields={
    'EMAIL': 'john.doe@example.com'
}, page=1, per_page=10)

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
ADD SUBSCRIBER
"""
response = endpoint.create(list_uid='LIST_UID', data={
    'EMAIL': 'john.doe@example.com',  # the confirmation email will be sent!!! Use valid email address
    'FNAME': 'John',
    'LNAME': 'Doe'
})

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
ADD SUBSCRIBERS IN BULK (since MailWizz 1.8.1)
"""
response = endpoint.create_bulk(list_uid='LIST_UID', data=[
    {
        'EMAIL': 'john.doe1@example.com',  # the confirmation email will be sent!!! Use valid email address
        'FNAME': 'John1',
        'LNAME': 'Doe1'
    },
    {
        'EMAIL': 'john.doe2@example.com',  # the confirmation email will be sent!!! Use valid email address
        'FNAME': 'John2',
        'LNAME': 'Doe2'
    },
    {
        'EMAIL': 'john.doe3@example.com',  # the confirmation email will be sent!!! Use valid email address
        'FNAME': 'John3',
        'LNAME': 'Doe3'
    },
])

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
UPDATE EXISTING SUBSCRIBER
"""
response = endpoint.update(list_uid='LIST_UID', subscriber_uid='SUBSCRIBER_UID', data={
    'EMAIL': 'john.doe.updated@example.com',  # the confirmation email will be sent!!! Use valid email address
    'FNAME': 'John Updated',
    'LNAME': 'Doe Updated'
})

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
CREATE / UPDATE EXISTING SUBSCRIBER
"""
response = endpoint.create_update(list_uid='LIST_UID', data={
    'EMAIL': 'xxxghimescosmin2@google.com',  # the confirmation email will be sent!!! Use valid email address
    'FNAME': 'John Updated',
    'LNAME': 'Doe Updated'
})

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
UNSUBSCRIBE existing subscriber, no email is sent, unsubscribe is silent
"""
response = endpoint.unsubscribe(list_uid='LIST_UID', subscriber_uid='SUBSCRIBER_UID')

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
UNSUBSCRIBE existing subscriber by email address, no email is sent, unsubscribe is silent
"""
response = endpoint.unsubscribe_by_email(list_uid='LIST_UID', email_address='john.doe@example.com')

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
UNSUBSCRIBE existing subscriber by email address from all lists, no email is sent, unsubscribe is silent
"""
response = endpoint.unsubscribe_by_email_from_all_lists(email_address='john.doe@example.com')

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
DELETE SUBSCRIBER, no email is sent, delete is silent
"""
response = endpoint.delete(list_uid='LIST_UID', subscriber_uid='SUBSCRIBER_UID')

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
DELETE SUBSCRIBER by email address, no email is sent, delete is silent
"""
response = endpoint.delete_by_email(list_uid='LIST_UID', email_address='john.doe@example.com')

"""
DISPLAY RESPONSE
"""
print(response.content)
