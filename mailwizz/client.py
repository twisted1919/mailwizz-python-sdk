from mailwizz.base import Base
from mailwizz.request import Request


class Client(Base):
    """
    Client is the http client interface used to make the remote requests and receive the responses.
    """

    # Marker for GET requests.
    METHOD_GET = 'GET'

    # Marker for POST requests
    METHOD_POST = 'POST'

    # Marker for PUT requests
    METHOD_PUT = 'PUT'

    # Marker for DELETE requests
    METHOD_DELETE = 'DELETE'

    # Marker for the client version
    CLIENT_VERSION = '1.0'

    # the method used in the request.
    method = METHOD_GET

    # the url where the remote calls will be made.
    url = ''

    # the default timeout for request.
    timeout = 30

    # the headers sent in the request.
    headers = {}

    # the GET params sent in the request.
    params_get = {}

    # the POST params sent in the request.
    params_post = {}

    # the PUT params sent in the request.
    params_put = {}

    # the DELETE params sent in the request.
    params_delete = {}

    def __init__(self, options):
        self.__populate(options)

    def request(self):
        """

        :return:
        """

        request = Request(self)
        return request.send()

    def is_get_method(self):
        """
        Check if the method is get
        :return: bool
        """

        return self.method.upper() == self.METHOD_GET

    def is_post_method(self):
        """
        Check if the method is post
        :return: bool
        """

        return self.method.upper() == self.METHOD_POST

    def is_put_method(self):
        """
        Check if the method is put
        :return: bool
        """

        return self.method.upper() == self.METHOD_PUT

    def is_delete_method(self):
        """
        Check if the method is delete
        :return: bool
        """

        return self.method.upper() == self.METHOD_DELETE

    def __populate(self, options):
        """
        Populate the class attributes from the options array
        :param options:
        :return:
        """

        if 'method' in options:
            self.method = options['method']

        if 'url' in options:
            self.url = options['url']
        else:
            raise ValueError('Please set the url where your request will be made.')

        if 'params_get' in options:
            self.params_get = options['params_get']

        if 'params_post' in options:
            self.params_post = options['params_post']

        if 'params_put' in options:
            self.params_put = options['params_put']

        if 'params_delete' in options:
            self.params_delete = options['params_delete']

        if 'headers' in options:
            self.headers = options['headers']
