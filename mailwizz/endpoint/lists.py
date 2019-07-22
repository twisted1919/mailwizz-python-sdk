from mailwizz.base import Base
from mailwizz.client import Client


class Lists(Base):
    """
    Lists handles all the API calls for lists.
    """

    def get_lists(self, page=1, per_page=10):
        """
        Get all the mail list of the current customer
        :param page:
        :param per_page:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('lists'),
            'params_get': {
                'page': page,
                'per_page': per_page
            }
        })

        return client.request()

    def get_list(self, list_uid: str):
        """
        Get one list
        :param list_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('lists/{list_uid}'.format(list_uid=list_uid)),
            'params_get': {}
        })

        return client.request()

    def create(self, data: dict):
        """
        Create a new mail list for the customer
        The data param must contain following keys:
            -> general
            -> defaults
            -> notifications
            -> company
        :param data:
        :return:
        """

        client = Client({
            'method': Client.METHOD_POST,
            'url': self.config.get_api_url('lists'),
            'params_post': self._prepare_body(data)
        })

        return client.request()

    def update(self, list_uid: str, data: dict):
        """
        Update one list
        :param list_uid:
        :param data:
        :return:
        """

        client = Client({
            'method': Client.METHOD_PUT,
            'url': self.config.get_api_url('lists/{list_uid}'.format(list_uid=list_uid)),
            'params_put': self._prepare_body(data)
        })

        return client.request()

    def copy(self, list_uid: str):
        """
        Copy one list
        :param list_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_POST,
            'url': self.config.get_api_url('lists/{list_uid}/copy'.format(list_uid=list_uid)),
        })

        return client.request()

    def delete(self, list_uid: str):
        """
        Delete one list
        :param list_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_DELETE,
            'url': self.config.get_api_url('lists/{list_uid}'.format(list_uid=list_uid)),
        })

        return client.request()
