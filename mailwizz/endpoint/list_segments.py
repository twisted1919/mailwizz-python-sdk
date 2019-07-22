from mailwizz.base import Base
from mailwizz.client import Client


class ListSegments(Base):
    """
    ListSegments handles all the API calls for handling the list segments.
    """

    def get_segments(self, list_uid: str, page=1, per_page=10):
        """
        Get segments from a certain mail list
        :param list_uid:
        :param page:
        :param per_page:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('lists/{list_uid}/segments'.format(list_uid=list_uid)),
            'params_get': {
                'page': page,
                'per_page': per_page
            }
        })

        return client.request()
