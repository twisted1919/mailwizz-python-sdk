import base64

from mailwizz.base import Base
from mailwizz.client import Client


class Templates(Base):
    """
    Templates handles all the API calls for email templates.
    """

    def get_templates(self, page=1, per_page=10):
        """
        Get all the email templates of the current customer
        :param page:
        :param per_page:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('templates'),
            'params_get': {
                'page': page,
                'per_page': per_page
            }
        })

        return client.request()

    def search_templates(self, page=1, per_page=10, filters=None):
        """
        Search through all the email templates of the current customer
        :param page:
        :param per_page:
        :param filters:
        :return:
        """

        if filters is None:
            filters = {}

        params_get = {
            'page': page,
            'per_page': per_page,
            'filter': filters
        }
        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('templates'),
            'params_get': super()._prepare_body(params_get)
        })

        return client.request()

    def get_template(self, template_uid: str):
        """
        Get one template
        :param template_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_GET,
            'url': self.config.get_api_url('templates/{template_uid}'.format(template_uid=template_uid)),
            'params_get': {}
        })

        return client.request()

    def create(self, data: dict):
        """
        Create a new template
        :param data:
        :return:
        """

        client = Client({
            'method': Client.METHOD_POST,
            'url': self.config.get_api_url('templates'),
            'params_post': self._prepare_body(data)
        })

        return client.request()

    def update(self, template_uid: str, data: dict):
        """
        Update one template
        :param template_uid:
        :param data:
        :return:
        """

        client = Client({
            'method': Client.METHOD_PUT,
            'url': self.config.get_api_url('templates/{template_uid}'.format(template_uid=template_uid)),
            'params_put': self._prepare_body(data)
        })

        return client.request()

    def delete(self, template_uid: str):
        """
        Delete one template
        :param template_uid:
        :return:
        """

        client = Client({
            'method': Client.METHOD_DELETE,
            'url': self.config.get_api_url('templates/{template_uid}'.format(template_uid=template_uid)),
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
            content = data['content']
            if content is not None:
                if type(content) is str:
                    content = bytes(content, 'utf-8')
                data['content'] = base64.b64encode(content)
        except KeyError:
            pass

        try:
            archive = data['archive']
            if archive is not None:
                if type(archive) is str:
                    archive = bytes(archive, 'utf-8')
                data['archive'] = base64.b64encode(archive)
        except KeyError:
            pass

        d = {}

        for key in data.keys():
            d['template[' + key + ']'] = data[key]

        return super()._prepare_body(d, default)
