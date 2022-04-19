class Base(object):
    """
    This file contains the base class for the Mailwizz Python-SDK.
    Base is the base class for all the other classes used in the sdk.
    """

    __config = {}

    @property
    def config(self):
        """
        Config the configuration object injected into the application at runtime
        :return:
        """

        return Base.__config

    @staticmethod
    def set_config(config):
        """
        Inject the configuration into the sdk
        :param config:
        :return:
        """

        Base.__config = config

    def _prepare_body(self, data: dict, default=None):
        """
        Builds the body of the data. Python cannot encode the data so it can be read correctly on the API side
        :param data:
        :param default:
        :return:
        """

        if default is None:
            default = {
                'general': {},
                'defaults': {},
                'notifications': {},
                'company': {},
                'options': {},
                'template': {},
                'filter': {},
                'details': {}
            }

        data = {**default, **data}

        d = {}

        for _id in default.keys():
            if _id in data:
                for key in data[_id]:
                    d[_id + '[' + key + ']'] = data[_id][key]
                data.pop(_id, None)

        return {**data, **d}
