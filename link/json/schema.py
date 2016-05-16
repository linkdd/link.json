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
    """
    Helper class used to validate data with the JSON Schema specification.

    See: http://json-schema.org
    """

    def __init__(self, *args, **kwargs):
        super(JsonSchema, self).__init__(*args, **kwargs)

        self.resolver = JsonResolver()

    def get(self, url):
        """
        Get schema pointed by URL.

        :param url: URL pointing to a schema
        :type url: str

        :returns: Schema
        :rtype: dict
        """

        return self.resolver({'$ref': url})

    def validate(self, schema_or_url, data):
        """
        Validate data against schema.

        :param schema_or_url: Schema used for validation, or URL pointing to it
        :type schema_or_url: dict or str

        :param data: Data to validate
        :type data: any

        :throws: JsonValidationError
        """

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
        """
        Check if data is validated by schema.

        :param schema_or_url: Schema used for validation, or URL pointing to it
        :type schema_or_url: dict or str

        :param data: Data to validate
        :type data: any

        :returns: ``True`` if data is valid, ``False`` otherwise
        :rtype: bool
        """

        try:
            self.validate(schema_or_url, data)

        except JsonValidationError:
            return False

        return True
