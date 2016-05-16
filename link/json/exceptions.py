# -*- coding: utf-8 -*-


class JsonError(Exception):
    pass


class JsonValidationError(JsonError):
    pass


class JsonTransformationError(JsonError):
    pass
