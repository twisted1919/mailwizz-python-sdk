from mailwizz.base import Base
from mailwizz.client import Client


class ListSubscribers(Base):
    """
    ListSubscribers handles all the API calls for lists subscribers.
    """

    def get_subscribers(self, list_uid: str, page=1, per_page=10):
        """
        Get subscribers from a certain mail list
        :param list_uid:
        :param page:
        :param per_page:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('lists/{list_uid}/subscribers'.format(list_uid=list_uid)),
            'params_get': {
                'page': page,
                'per_page': per_page
            }
        })

        return client.request()

    def get_subscriber(self, list_uid: str, subscriber_uid: str):
        """
        Get one subscriber from a certain mail list
        :param list_uid:
        :param subscriber_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url(
                'lists/{list_uid}/subscribers/{subscriber_uid}'.format(
                    list_uid=list_uid,
                    subscriber_uid=subscriber_uid
                )
            ),
            'params_get': {}
        })

        return client.request()

    def create(self, list_uid: str, data: dict):
        """
        Create a new subscriber in the given list
        :param list_uid:
        :param data:
        :return:
        """

        client = Client({
            'method': Client.METHOD_POST,
            'url': self.config.get_api_url('lists/{list_uid}/subscribers'.format(list_uid=list_uid)),
            'params_post': super()._prepare_body(data)
        })

        return client.request()

    def create_bulk(self, list_uid: str, data):
        """
        Create subscribers in bulk in the given list
        This feature is available since  1.8.1
        :param list_uid:
        :param data:
        :return:
        """

        client = Client({
            'method': Client.METHOD_POST,
            'url': self.config.get_api_url('lists/{list_uid}/subscribers/bulk'.format(list_uid=list_uid)),
            'params_post': self._prepare_body(data)
        })

        return client.request()

    def update(self, list_uid: str, subscriber_uid: str, data: dict):
        """
        Update existing subscriber in given list
        :param list_uid:
        :param subscriber_uid:
        :param data:
        :return:
        """

        client = Client({
            'method': Client.METHOD_PUT,
            'url': self.config.get_api_url(
                'lists/{list_uid}/subscribers/{subscriber_uid}'.format(
                    list_uid=list_uid,
                    subscriber_uid=subscriber_uid
                )
            ),
            'params_put': data
        })

        return client.request()

    def unsubscribe(self, list_uid: str, subscriber_uid: str):
        """
        Unsubscribe existing subscriber from given list
        :param list_uid:
        :param subscriber_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_PUT,
            'url': self.config.get_api_url(
                'lists/{list_uid}/subscribers/{subscriber_uid}/unsubscribe'.format(
                    list_uid=list_uid,
                    subscriber_uid=subscriber_uid
                )
            ),
            'params_put': {}
        })

        return client.request()

    def unsubscribe_by_email(self, list_uid: str, email_address: str):
        """
        Unsubscribe existing subscriber by email address
        :param list_uid:
        :param email_address:
        :return:
        """

        response = self.email_search(list_uid, email_address)

        if not response:
            return response

        content = response.json()
        body_data = content['data']

        if content['status'] == 'error' or len(body_data) == 0:
            return response

        if not body_data['subscriber_uid']:
            return response

        return self.unsubscribe(list_uid, body_data['subscriber_uid'])

    def unsubscribe_by_email_from_all_lists(self, email_address: str):
        """
        Unsubscribe existing subscriber by email address from all lists
        :param email_address:
        :return:
        """

        client = Client({
            'method': Client.METHOD_PUT,
            'url': self.config.get_api_url('lists/subscribers/unsubscribe-by-email-from-all-lists'),
            'params_put': {
                'EMAIL': email_address
            }
        })

        return client.request()

    def delete(self, list_uid: str, subscriber_uid: str):
        """
        Delete existing subscriber from given list
        :param list_uid:
        :param subscriber_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_DELETE,
            'url': self.config.get_api_url(
                'lists/{list_uid}/subscribers/{subscriber_uid}'.format(
                    list_uid=list_uid,
                    subscriber_uid=subscriber_uid
                )
            ),
            'params_delete': {}
        })

        return client.request()

    def delete_by_email(self, list_uid: str, email_address: str):
        """
        Delete existing subscriber by email address
        :param list_uid:
        :param email_address:
        :return:
        """

        response = self.email_search(list_uid, email_address)

        content = response.json()

        if content['status'] == 'error':
            return response

        try:
            body_data = content['data']
            subscriber_uid = body_data['subscriber_uid']
        except KeyError:
            return response

        if not subscriber_uid:
            return response

        return self.delete(list_uid, subscriber_uid)

    def email_search(self, list_uid: str, email_address: str):
        """
        Search in a list for given subscriber by email address
        :param list_uid:
        :param email_address:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('lists/{list_uid}/subscribers/search-by-email'.format(list_uid=list_uid)),
            'params_get': {
                'EMAIL': email_address
            }
        })

        return client.request()

    def email_search_all_lists(self, email_address: str):
        """
        Search in a all lists for given subscriber by email address
        Please note that this is available only for mailwizz >= 1.3.6.2
        :param email_address:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('lists/subscribers/search-by-email-in-all-lists'),
            'params_get': {
                'EMAIL': email_address
            }
        })

        return client.request()

    def search_by_custom_fields(self, list_uid: str, fields: dict, page=1, per_page=10):
        """
        Search in a list by custom fields
        :param list_uid:
        :param fields:
        :param page:
        :param per_page:
        :return:
        """

        params_get = fields
        params_get[page] = page
        params_get[per_page] = per_page

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url(
                'lists/{list_uid}/subscribers/search-by-custom-fields'.format(list_uid=list_uid)),
            'params_get': params_get
        })

        return client.request()

    def create_update(self, list_uid: str, data: dict):
        """
        Create or update a subscriber in given list
        :param list_uid:
        :param data:
        :return:
        """

        email_address = None

        try:
            email_address = data['EMAIL']
        except KeyError:
            pass

        response = self.email_search(list_uid, email_address)

        content = response.json()

        if content['status'] == 'error':
            return self.create(list_uid, data)

        try:
            body_data = content['data']
            subscriber_uid = body_data['subscriber_uid']
        except KeyError:
            return response

        if not subscriber_uid:
            return response

        return self.update(list_uid, subscriber_uid, data)

    def _prepare_body(self, data, default=None):
        """
        Builds the body of the data. Python cannot encode the data so it can be read correctly on the API side
        :param data:
        :param default:
        :return:
        """

        d = {}
        i = 0
        for item in data:
            for key in item.keys():
                d['subscribers[' + str(i) + '][' + key + ']'] = item[key]
            i = i + 1

        return d
