# -*- coding: utf-8 -*-

from b3j0f.conf import Configurable, category

from link.json.exceptions import JsonValidationError
from link.json.resolver import JsonResolver
from link.json import CONF_BASE_PATH

from jsonschema import validate, ValidationError
from six import string_types, raise_from


@Configurable(
    paths='{0}/schema.conf'.format(CONF_BASE_PATH),
    conf=category('JSONSCHEMA')
)
class JsonSchema(object):
    def __init__(self, *args, **kwargs):
        super(JsonSchema, self).__init__(*args, **kwargs)

        self.resolver = JsonResolver()

    def get(self, url):
        return self.resolver({'$ref': url})

    def validate(self, schema_or_url, data):
        if isinstance(schema_or_url, string_types):
            schema = self.get(schema_or_url)

        else:
            schema = schema_or_url

        try:
            validate(data, schema)

        except ValidationError as err:
            raise_from(
                JsonValidationError(str(err)),
                err
            )

    def isvalid(self, schema_or_url, data):
        try:
            self.validate(schema_or_url, data)

        except JsonValidationError:
            return False

        return True
