from setup_api import setup
from mailwizz.endpoint.templates import Templates

"""
SETUP THE API
"""
setup()

"""
CREATE THE ENDPOINT
"""
endpoint = Templates()


"""
GET ONE ITEM
"""
response = endpoint.get_template(template_uid='TEMPLATE_UID')

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
GET ALL TEMPLATES
"""
response = endpoint.get_templates(page=1, per_page=10)

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
SEARCH FOR TEMPLATES
"""
response = endpoint.search_templates(page=1, per_page=10, filters={
    'name': 'example-template'
})

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
CREATE ONE TEMPLATE
"""
response = endpoint.create(data={
    'name': 'My API template ',
    # 'content': '<body>Hello</body>',
    # 'content': open('template-example.html', 'rb').read(),
    'archive': open('template-example.zip', 'rb').read(),
    'inline_css': 'no',  # yes|no
})

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
UPDATE ONE TEMPLATE
"""
response = endpoint.update(template_uid='TEMPLATE_UID', data={
    'name': 'My API template - Updated',
    # 'content': open('template-example.html', 'rb').read(),
    # 'archive': open('template-example.zip', 'rb').read(),
    'inline_css': 'no',  # yes|no
})

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
DELETE A TEMPLATE
"""
response = endpoint.delete('TEMPLATE_UID')

"""
DISPLAY RESPONSE
"""
print(response.content)
