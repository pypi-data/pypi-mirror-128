# coding: utf-8

"""
    EVR API

    OpenAPI Generator'i jaoks kohandatud EVR API kirjeldus. Kasuta seda juhul, kui spetsifikatsioonile vastava EVR API kirjeldusega ei õnnestu klienti genereerida.  # noqa: E501

    The version of the OpenAPI document: 1.5.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pyevr.openapi_client.configuration import Configuration


class PagedResultOfWaybill(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'page_number': 'int',
        'page_size': 'int',
        'page_result': 'list[Waybill]',
        'total_count': 'int'
    }

    attribute_map = {
        'page_number': 'pageNumber',
        'page_size': 'pageSize',
        'page_result': 'pageResult',
        'total_count': 'totalCount'
    }

    def __init__(self, page_number=None, page_size=None, page_result=None, total_count=None, local_vars_configuration=None):  # noqa: E501
        """PagedResultOfWaybill - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._page_number = None
        self._page_size = None
        self._page_result = None
        self._total_count = None
        self.discriminator = None

        if page_number is not None:
            self.page_number = page_number
        if page_size is not None:
            self.page_size = page_size
        if page_result is not None:
            self.page_result = page_result
        if total_count is not None:
            self.total_count = total_count

    @property
    def page_number(self):
        """Gets the page_number of this PagedResultOfWaybill.  # noqa: E501


        :return: The page_number of this PagedResultOfWaybill.  # noqa: E501
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """Sets the page_number of this PagedResultOfWaybill.


        :param page_number: The page_number of this PagedResultOfWaybill.  # noqa: E501
        :type: int
        """

        self._page_number = page_number

    @property
    def page_size(self):
        """Gets the page_size of this PagedResultOfWaybill.  # noqa: E501


        :return: The page_size of this PagedResultOfWaybill.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this PagedResultOfWaybill.


        :param page_size: The page_size of this PagedResultOfWaybill.  # noqa: E501
        :type: int
        """

        self._page_size = page_size

    @property
    def page_result(self):
        """Gets the page_result of this PagedResultOfWaybill.  # noqa: E501


        :return: The page_result of this PagedResultOfWaybill.  # noqa: E501
        :rtype: list[Waybill]
        """
        return self._page_result

    @page_result.setter
    def page_result(self, page_result):
        """Sets the page_result of this PagedResultOfWaybill.


        :param page_result: The page_result of this PagedResultOfWaybill.  # noqa: E501
        :type: list[Waybill]
        """

        self._page_result = page_result

    @property
    def total_count(self):
        """Gets the total_count of this PagedResultOfWaybill.  # noqa: E501


        :return: The total_count of this PagedResultOfWaybill.  # noqa: E501
        :rtype: int
        """
        return self._total_count

    @total_count.setter
    def total_count(self, total_count):
        """Sets the total_count of this PagedResultOfWaybill.


        :param total_count: The total_count of this PagedResultOfWaybill.  # noqa: E501
        :type: int
        """

        self._total_count = total_count

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PagedResultOfWaybill):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PagedResultOfWaybill):
            return True

        return self.to_dict() != other.to_dict()
