from mailwizz.base import Base
from mailwizz.client import Client


class Countries(Base):
    """
    Countries handles all the API calls for handling the countries and their zones.
    """

    def get_countries(self, page=1, per_page=10):
        """
        Get all available countries
        :param page:
        :param per_page:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('countries'),
            'params_get': {
                'page': page,
                'per_page': per_page
            }
        })

        return client.request()

    def get_zones(self, country_id, page=1, per_page=10):
        """
        Get all available country zones
        :param country_id:
        :param page:
        :param per_page:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('countries/{country_id}/zones'.format(country_id=country_id)),
            'params_get': {
                'page': page,
                'per_page': per_page
            }
        })

        return client.request()
