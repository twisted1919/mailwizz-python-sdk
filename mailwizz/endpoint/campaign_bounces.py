from mailwizz.base import Base
from mailwizz.client import Client


class CampaignBounces(Base):
    """
     CampaignBounces handles all the API calls for campaigns bounces.
    """

    def get_bounces(self, campaign_uid: str, page=1, per_page=10):
        """
        Get bounces from a certain campaign
        :param campaign_uid:
        :param page:
        :param per_page:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('campaigns/{campaign_uid}/bounces'.format(campaign_uid=campaign_uid)),
            'params_get': {
                'page': page,
                'per_page': per_page
            }
        })

        return client.request()

    def create(self, campaign_uid: str, data: dict):
        """
        Create a new bounce in the given campaign
        :param campaign_uid:
        :param data:
        :return:
        """

        client = Client({
            'method': Client.METHOD_POST,
            'url': self.config.get_api_url('campaigns/{campaign_uid}/bounces'.format(campaign_uid=campaign_uid)),
            'params_post': self._prepare_body(data)
        })

        return client.request()
