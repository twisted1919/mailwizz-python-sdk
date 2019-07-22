from urllib.parse import urlparse

from mailwizz.base import Base


class Config(Base):
    """
    Config contains the configuration class that is injected at runtime into the main application.
    It's only purpose is to set the needed data so that the API calls will run without problems.
    """

    def __init__(self, config=None):
        if config:
            self.api_url = config['api_url']
            self.public_key = config['public_key']
            self.private_key = config['private_key']
            self.charset = config['charset']

    @property
    def api_url(self):
        """
        Getter for the api_url
        :return:
        """

        if not self.__api_url:
            raise ValueError('Please set the api base url.')

        return self.__api_url

    @api_url.setter
    def api_url(self, url):
        """
        Setter for the api_url
        :param url:
        :return:
        """

        parse_results = urlparse(url)

        if len(parse_results.scheme) == 0 or len(parse_results.netloc) == 0:
            raise ValueError('Please set a valid api base url.')

        self.__api_url = url.rstrip('/') + '/'

    def get_api_url(self, endpoint=None):
        """
        Setter for the endpoint api url
        :param endpoint:
        :return:
        """

        if not self.api_url or endpoint is None:
            raise ValueError('Please set the api base url.')

        return str(self.api_url) + str(endpoint)
