import base64

from mailwizz.base import Base
from mailwizz.client import Client


class Campaigns(Base):
    """
    Campaigns handles all the API calls for campaigns.
    """

    def get_campaigns(self, page=1, per_page=10):
        """
        Get all the campaigns of the current customer
        :param page:
        :param per_page:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('campaigns'),
            'params_get': {
                'page': page,
                'per_page': per_page
            }
        })

        return client.request()

    def get_campaign(self, campaign_uid: str):
        """
        Get one campaign
        :param campaign_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('campaigns/{campaign_uid}'.format(campaign_uid=campaign_uid)),
            'params_get': {}
        })

        return client.request()

    def create(self, data: dict):
        """
        Create a new campaign
        :param data:
        :return:
        """

        client = Client({
            'method': Client.METHOD_POST,
            'url': self.config.get_api_url('campaigns'),
            'params_post': self._prepare_body(data)
        })

        return client.request()

    def update(self, campaign_uid: str, data: dict):
        """
        Update one campaign
        :param campaign_uid:
        :param data:
        :return:
        """

        client = Client({
            'method': Client.METHOD_PUT,
            'url': self.config.get_api_url('campaigns/{campaign_uid}'.format(campaign_uid=campaign_uid)),
            'params_put': self._prepare_body(data)
        })

        return client.request()

    def copy(self, campaign_uid: str):
        """
        Copy one campaign
        :param campaign_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_POST,
            'url': self.config.get_api_url('campaigns/{campaign_uid}/copy'.format(campaign_uid=campaign_uid)),
        })

        return client.request()

    def pause_unpause(self, campaign_uid: str):
        """
        Pause/Unpause one campaign
        :param campaign_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_PUT,
            'url': self.config.get_api_url('campaigns/{campaign_uid}/pause-unpause'.format(campaign_uid=campaign_uid)),
        })

        return client.request()

    def mark_sent(self, campaign_uid: str):
        """
        Mark as sent one campaign
        :param campaign_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_PUT,
            'url': self.config.get_api_url('campaigns/{campaign_uid}/mark-sent'.format(campaign_uid=campaign_uid)),
        })

        return client.request()

    def delete(self, campaign_uid: str):
        """
        Delete one campaign
        :param campaign_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_DELETE,
            'url': self.config.get_api_url('campaigns/{campaign_uid}'.format(campaign_uid=campaign_uid)),
        })

        return client.request()

    def _prepare_body(self, data, default=None):
        """
        Builds the body of the data. Python cannot encode the data so it can be read correctly on the API side
        :param data:
        :param default:
        :return:
        """

        try:
            content = data['template']['content']
            if content is not None:
                if type(content) is str:
                    content = bytes(content, 'utf-8')
                data['template']['content'] = base64.b64encode(content)
        except KeyError:
            pass

        try:
            archive = data['template']['archive']
            if archive is not None:
                if type(archive) is str:
                    archive = bytes(archive, 'utf-8')
                data['template']['archive'] = base64.b64encode(archive)
        except KeyError:
            pass

        try:
            text = data['template']['plain_text']
            if text is not None:
                if type(text) is str:
                    text = bytes(text, 'utf-8')
                data['template']['plain_text'] = base64.b64encode(text)
        except KeyError:
            pass

        if default is None:
            default = {
                'campaign[options]': {},
                'campaign[template]': {},
            }

        d = {}

        for key in data.keys():
            d['campaign[' + key + ']'] = data[key]

        return super()._prepare_body(d, default)
