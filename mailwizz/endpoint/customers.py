from mailwizz.base import Base
from mailwizz.client import Client


class Customers(Base):
    """
    Customers handles all the API calls for customers.
    """

    def create(self, data: dict):
        """
        Create a new customer
        :param data:
        :return:
        """

        client = Client({
            'method': Client.METHOD_POST,
            'url': self.config.get_api_url('customers'),
            'params_post': self._prepare_body(data)
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
            data['customer']['confirm_password'] = data['customer']['password']
        except KeyError:
            pass

        try:
            data['customer']['confirm_email'] = data['customer']['email']
        except KeyError:
            pass

        try:
            timezone = data['customer']['timezone']
            if timezone is None:
                data['customer']['timezone'] = 'UTC'
        except KeyError:
            pass

        if default is None:
            default = {
                'customer': {},
                'company': {},
            }

        return super()._prepare_body(data, default)
