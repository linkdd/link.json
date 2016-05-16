# -*- coding: utf-8 -*-

from b3j0f.conf import Configurable, category

from link.json.exceptions import JsonTransformationError
from link.json.resolver import JsonResolver
from link.json.schema import JsonSchema
from link.json import CONF_BASE_PATH

from jsonpatch import JsonPatch, JsonPatchException
from six import string_types, raise_from


@Configurable(
    paths='{0}/transform.conf'.format(CONF_BASE_PATH),
    conf=category('JSONTRANSFORM')
)
class JsonTransform(object):
    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        if isinstance(value, string_types):
            value = self.resolver({'$ref': value})

        self._source = value

    @property
    def patch(self):
        return self._patch

    @patch.setter
    def patch(self, value):
        if isinstance(value, string_types):
            value = self.resolver({'$ref': value})

        self._patch = JsonPatch(value)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        if isinstance(value, string_types):
            value = self.resolver({'$ref': value})

        self._target = value

    def __init__(self, source, patch, target, *args, **kwargs):
        super(JsonSchema, self).__init__(*args, **kwargs)

        self.resolver = JsonResolver()
        self.validator = JsonSchema()

        self.source = source
        self.patch = patch
        self.target = target

    def __call__(self, data):
        self.source.validate(data)

        try:
            result = self.patch.apply(data)

        except JsonPatchException as err:
            raise_from(
                JsonTransformationError(str(err)),
                err
            )

        self.target.validate(result)

        return result
