from setup_api import setup
from mailwizz.endpoint.campaign_bounces import CampaignBounces


"""
SETUP THE API
"""
setup()

"""
CREATE THE ENDPOINT
"""
endpoint = CampaignBounces()

"""
GET ALL ITEMS
"""
response = endpoint.get_bounces(campaign_uid='CAMPAIGN_UID', page=1, per_page=10)

"""
DISPLAY RESPONSE
"""
print(response.content)

"""
CREATE BOUNCE
"""
response = endpoint.create('CAMPAIGN_UID', {
    # required
    'message': 'The reason why this email bounced',
    'bounce_type': 'hard',
    'subscriber_uid': 'SUBSCRIBER_UID'
})

"""
DISPLAY RESPONSE
"""
print(response.content)
