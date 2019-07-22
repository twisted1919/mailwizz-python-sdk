from mailwizz.base import Base
from mailwizz.client import Client


class CampaignsTracking(Base):
    """
    CampaignsTracking handles all the API calls for campaigns tracking.
    """

    def track_url(self, campaign_uid: str, subscriber_uid: str, hash_string: str):
        """
        Track campaign url click for certain subscriber
        :param campaign_uid:
        :param subscriber_uid:
        :param hash_string:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url(
                'campaigns/{campaign_uid}/track-url/{subscriber_uid}/{hash_string}'.format(
                    campaign_uid=campaign_uid,
                    subscriber_uid=subscriber_uid,
                    hash_string=hash_string
                )
            ),
            'params_get': {}
        })

        return client.request()

    def track_opening(self, campaign_uid: str, subscriber_uid: str):
        """
        Track campaign url click for certain subscriber
        :param campaign_uid:
        :param subscriber_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url(
                'campaigns/{campaign_uid}/track-opening/{subscriber_uid}'.format(
                    campaign_uid=campaign_uid,
                    subscriber_uid=subscriber_uid
                )
            ),
            'params_get': {}
        })

        return client.request()

    def track_unsubscribe(self, campaign_uid: str, subscriber_uid: str, data: dict):
        """
        Track campaign unsubscribe for certain subscriber
        :param campaign_uid:
        :param subscriber_uid:
        :param data:
        :return:
        """

        client = Client({
            'method': Client.METHOD_POST,
            'url': self.config.get_api_url(
                'campaigns/{campaign_uid}/track-unsubscribe/{subscriber_uid}'.format(
                    campaign_uid=campaign_uid,
                    subscriber_uid=subscriber_uid
                )
            ),
            'params_post': self._prepare_body(data)
        })

        return client.request()
