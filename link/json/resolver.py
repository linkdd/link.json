# -*- coding: utf-8 -*-

from b3j0f.conf import Configurable, category
from b3j0f.middleware import fromurl

from link.json import CONF_BASE_PATH

from jsonpointer import resolve_pointer
import json


@Configurable(
    paths='{0}/resolver.conf'.format(CONF_BASE_PATH),
    conf=category('JSONRESOLVER')
)
class JsonResolver(object):
    """
    Resolve JSON references.

    See: https://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03
    """

    def resolve(self, url):
        """
        Returns document pointed by URL.

        :param url: URL pointing to a JSON document
        :type url: str

        :return: Pointed document or value
        :rtype: any
        """

        middleware = fromurl(url)[0]
        data = json.loads(middleware.get())

        if middleware.fragment:
            data = resolve_pointer(data, middleware.fragment)

        return data

    def _resolve_nested(self, root, data):
        """
        Internal method for walking through data.

        :param root: Data to resolve recursively
        :type root: any

        :param data: Data being resolved
        :type data: any

        :return: Data with nested references resolved
        :rtype: any
        """

        if isinstance(data, dict) and '$ref' in data:
            url = data.pop('$ref')

            if url[0] == '#':
                refdata = resolve_pointer(root, url[1:])

            else:
                refdata = self.resolve(url)

            data = refdata

        if isinstance(data, dict):
            for key in data:
                data[key] = self._resolve_nested(root, data[key])

        elif isinstance(data, list):
            for i in range(len(data)):
                data[i] = self._resolve_nested(root, data[i])

        return data

    def __call__(self, data):
        """
        Walk through data and resolve every found reference.

        :param data: Data to resolve recursively
        :type data: any

        :return: Data with nested references resolved
        :rtype: any
        """
        return self._resolve_nested(data, data)
