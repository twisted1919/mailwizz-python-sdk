from setup_api import setup
from mailwizz.endpoint.campaigns_tracking import CampaignsTracking

"""
SETUP THE API
"""
setup()

"""
CREATE THE ENDPOINT
"""
endpoint = CampaignsTracking()

"""
Track subscriber click for campaign click
"""
response = endpoint.track_url(campaign_uid='CAMPAIGN_UID', subscriber_uid='SUBSCRIBER_UID', hash_string='')

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
Track subscriber open for campaign
"""
response = endpoint.track_opening(campaign_uid='CAMPAIGN_UID', subscriber_uid='SUBSCRIBER_UID')

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
Track subscriber unsubscribe for campaign
"""
response = endpoint.track_unsubscribe(campaign_uid='CAMPAIGN_UID', subscriber_uid='SUBSCRIBER_UID', data={
    'ip_address': '123.123.123.123',
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'reason': 'Reason for unsubscribe!',
})

"""
DISPLAY RESPONSE
"""
print(response.content)