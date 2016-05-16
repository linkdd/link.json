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
    def resolve(self, url):
        middleware = fromurl(url)
        data = json.loads(middleware.get())

        if middleware.fragment:
            data = resolve_pointer(data, middleware.fragment)

        return data

    def _resolve_nested(self, data):
        if isinstance(data, dict) and '$ref' in data:
            url = data.pop('$ref')
            refdata = self.resolve(url)
            data = refdata

        if isinstance(data, dict):
            for key in data:
                data[key] = self._resolve_nested(data[key])

        elif isinstance(data, list):
            for i in range(len(data)):
                data[i] = self._resolve_nested(data[i])

        return data

    def __call__(self, data):
        return self._resolve_nested(data)
