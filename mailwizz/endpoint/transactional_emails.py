import base64

from mailwizz.base import Base
from mailwizz.client import Client


class TransactionalEmails(Base):
    """
    TransactionalEmails handles all the API calls for transactional emails.
    """

    def get_emails(self, page=1, per_page=10):
        """
        Get all transactional emails of the current customer
        :param page:
        :param per_page:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('transactional-emails'),
            'params_get': {
                'page': page,
                'per_page': per_page
            }
        })

        return client.request()

    def get_email(self, email_uid: str):
        """
        Get one email
        :param email_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('transactional-emails/{email_uid}'.format(email_uid=email_uid)),
            'params_get': {}
        })

        return client.request()

    def create(self, data: dict):
        """
        Create a new email
        :param data:
        :return:
        """

        client = Client({
            'method': Client.METHOD_POST,
            'url': self.config.get_api_url('transactional-emails'),
            'params_post': self._prepare_body(data)
        })

        return client.request()

    def delete(self, email_uid: str):
        """
        Delete one email
        :param email_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_DELETE,
            'url': self.config.get_api_url('transactional-emails/{email_uid}'.format(email_uid=email_uid)),
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
            content = data['email']['body']
            if content is not None:
                data['email']['body'] = base64.b64encode(bytes(data['email']['body']))
        except KeyError:
            pass

        try:
            archive = data['email']['plain_text']
            if archive is not None:
                data['email']['plain_text'] = base64.b64encode(bytes(data['email']['plain_text']))
        except KeyError:
            pass

        d = {}

        for key in data.keys():
            d['email[' + key + ']'] = data[key]

        return super()._prepare_body(d, default)
