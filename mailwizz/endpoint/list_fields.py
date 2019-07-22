from mailwizz.base import Base
from mailwizz.client import Client


class ListFields(Base):
    """
    ListFields handles all the API calls for handling the list custom fields.
    """

    def get_fields(self, list_uid: str):
        """
        Get fields from a certain mail list
        :param list_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('lists/{list_uid}/fields'.format(list_uid=list_uid)),
            'params_get': {}
        })

        return client.request()
