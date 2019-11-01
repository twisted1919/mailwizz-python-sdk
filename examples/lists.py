from setup_api import setup
from mailwizz.endpoint.lists import Lists

"""
SETUP THE API
"""
setup()

"""
CREATE THE ENDPOINT
"""
endpointLists = Lists()


"""
"""
response = endpointLists.get_lists(page=1, per_page=10)

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
GET ONE ITEM
"""
response = endpointLists.get_list('LIST_UID')

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
CREATE ONE LIST
"""
response = endpointLists.create({
    # required
    'general': {
        'name': 'My list created from the API',  # required
        'description': 'This is a test list, created from the API.',  # required
    },
    'defaults': {
        'from_name': 'John Doe',  # required
        'from_email': 'johndoe@doe.com',  # required
        'reply_to': 'johndoe@doe.com',  # required
        'subject': 'Hello!',
    }
})

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
UPDATE ONE LIST
"""
response = endpointLists.update('LIST_UID', {
    # required
    'general': {
        'name': 'My list created from the API and now updated',  # required
        'description': 'This is a test list, created from the API.',  # required
    },
    'defaults': {
        'from_name': 'John Doe',  # required
        'from_email': 'johndoe@doe.com',  # required
        'reply_to': 'johndoe@doe.com',  # required
        'subject': 'Hello!',
    }
})

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
COPY A LIST
"""
response = endpointLists.copy('LIST_UID')

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
DELETE A LIST
"""
response = endpointLists.delete('LIST_UID')

"""
DISPLAY RESPONSE
"""
print(response.content)
