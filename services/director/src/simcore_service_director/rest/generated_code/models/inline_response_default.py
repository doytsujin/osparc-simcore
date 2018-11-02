# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from .base_model_ import Model
from .inline_response_default_error import InlineResponseDefaultError  # noqa: F401,E501
from .. import util


class InlineResponseDefault(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, data: object=None, error: InlineResponseDefaultError=None):  # noqa: E501
        """InlineResponseDefault - a model defined in OpenAPI

        :param data: The data of this InlineResponseDefault.  # noqa: E501
        :type data: object
        :param error: The error of this InlineResponseDefault.  # noqa: E501
        :type error: InlineResponseDefaultError
        """
        self.openapi_types = {
            'data': object,
            'error': InlineResponseDefaultError
        }

        self.attribute_map = {
            'data': 'data',
            'error': 'error'
        }

        self._data = data
        self._error = error

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponseDefault':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_default of this InlineResponseDefault.  # noqa: E501
        :rtype: InlineResponseDefault
        """
        return util.deserialize_model(dikt, cls)

    @property
    def data(self) -> object:
        """Gets the data of this InlineResponseDefault.


        :return: The data of this InlineResponseDefault.
        :rtype: object
        """
        return self._data

    @data.setter
    def data(self, data: object):
        """Sets the data of this InlineResponseDefault.


        :param data: The data of this InlineResponseDefault.
        :type data: object
        """

        self._data = data

    @property
    def error(self) -> InlineResponseDefaultError:
        """Gets the error of this InlineResponseDefault.


        :return: The error of this InlineResponseDefault.
        :rtype: InlineResponseDefaultError
        """
        return self._error

    @error.setter
    def error(self, error: InlineResponseDefaultError):
        """Sets the error of this InlineResponseDefault.


        :param error: The error of this InlineResponseDefault.
        :type error: InlineResponseDefaultError
        """

        self._error = error