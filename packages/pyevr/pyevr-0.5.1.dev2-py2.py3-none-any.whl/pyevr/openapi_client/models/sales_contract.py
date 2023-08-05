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


class SalesContract(object):
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
        'contract_number': 'str',
        'contract_date': 'datetime',
        'cadaster': 'str',
        'compartment': 'str',
        'forest_allocation_number': 'str',
        'previous_owner': 'PreviousOwner'
    }

    attribute_map = {
        'contract_number': 'contractNumber',
        'contract_date': 'contractDate',
        'cadaster': 'cadaster',
        'compartment': 'compartment',
        'forest_allocation_number': 'forestAllocationNumber',
        'previous_owner': 'previousOwner'
    }

    def __init__(self, contract_number=None, contract_date=None, cadaster=None, compartment=None, forest_allocation_number=None, previous_owner=None, local_vars_configuration=None):  # noqa: E501
        """SalesContract - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._contract_number = None
        self._contract_date = None
        self._cadaster = None
        self._compartment = None
        self._forest_allocation_number = None
        self._previous_owner = None
        self.discriminator = None

        self.contract_number = contract_number
        self.contract_date = contract_date
        self.cadaster = cadaster
        self.compartment = compartment
        self.forest_allocation_number = forest_allocation_number
        self.previous_owner = previous_owner

    @property
    def contract_number(self):
        """Gets the contract_number of this SalesContract.  # noqa: E501

        Dokumendi number  # noqa: E501

        :return: The contract_number of this SalesContract.  # noqa: E501
        :rtype: str
        """
        return self._contract_number

    @contract_number.setter
    def contract_number(self, contract_number):
        """Sets the contract_number of this SalesContract.

        Dokumendi number  # noqa: E501

        :param contract_number: The contract_number of this SalesContract.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and contract_number is None:  # noqa: E501
            raise ValueError("Invalid value for `contract_number`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                contract_number is not None and len(contract_number) > 500):
            raise ValueError("Invalid value for `contract_number`, length must be less than or equal to `500`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                contract_number is not None and len(contract_number) < 0):
            raise ValueError("Invalid value for `contract_number`, length must be greater than or equal to `0`")  # noqa: E501

        self._contract_number = contract_number

    @property
    def contract_date(self):
        """Gets the contract_date of this SalesContract.  # noqa: E501

        Dokumendi kuupäev  # noqa: E501

        :return: The contract_date of this SalesContract.  # noqa: E501
        :rtype: datetime
        """
        return self._contract_date

    @contract_date.setter
    def contract_date(self, contract_date):
        """Sets the contract_date of this SalesContract.

        Dokumendi kuupäev  # noqa: E501

        :param contract_date: The contract_date of this SalesContract.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and contract_date is None:  # noqa: E501
            raise ValueError("Invalid value for `contract_date`, must not be `None`")  # noqa: E501

        self._contract_date = contract_date

    @property
    def cadaster(self):
        """Gets the cadaster of this SalesContract.  # noqa: E501

        Katastritunnus  # noqa: E501

        :return: The cadaster of this SalesContract.  # noqa: E501
        :rtype: str
        """
        return self._cadaster

    @cadaster.setter
    def cadaster(self, cadaster):
        """Sets the cadaster of this SalesContract.

        Katastritunnus  # noqa: E501

        :param cadaster: The cadaster of this SalesContract.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and cadaster is None:  # noqa: E501
            raise ValueError("Invalid value for `cadaster`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                cadaster is not None and len(cadaster) > 500):
            raise ValueError("Invalid value for `cadaster`, length must be less than or equal to `500`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                cadaster is not None and len(cadaster) < 0):
            raise ValueError("Invalid value for `cadaster`, length must be greater than or equal to `0`")  # noqa: E501

        self._cadaster = cadaster

    @property
    def compartment(self):
        """Gets the compartment of this SalesContract.  # noqa: E501

        Kvartal  # noqa: E501

        :return: The compartment of this SalesContract.  # noqa: E501
        :rtype: str
        """
        return self._compartment

    @compartment.setter
    def compartment(self, compartment):
        """Sets the compartment of this SalesContract.

        Kvartal  # noqa: E501

        :param compartment: The compartment of this SalesContract.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                compartment is not None and len(compartment) > 200):
            raise ValueError("Invalid value for `compartment`, length must be less than or equal to `200`")  # noqa: E501

        self._compartment = compartment

    @property
    def forest_allocation_number(self):
        """Gets the forest_allocation_number of this SalesContract.  # noqa: E501

        Metsaeraldis  # noqa: E501

        :return: The forest_allocation_number of this SalesContract.  # noqa: E501
        :rtype: str
        """
        return self._forest_allocation_number

    @forest_allocation_number.setter
    def forest_allocation_number(self, forest_allocation_number):
        """Sets the forest_allocation_number of this SalesContract.

        Metsaeraldis  # noqa: E501

        :param forest_allocation_number: The forest_allocation_number of this SalesContract.  # noqa: E501
        :type: str
        """

        self._forest_allocation_number = forest_allocation_number

    @property
    def previous_owner(self):
        """Gets the previous_owner of this SalesContract.  # noqa: E501


        :return: The previous_owner of this SalesContract.  # noqa: E501
        :rtype: PreviousOwner
        """
        return self._previous_owner

    @previous_owner.setter
    def previous_owner(self, previous_owner):
        """Sets the previous_owner of this SalesContract.


        :param previous_owner: The previous_owner of this SalesContract.  # noqa: E501
        :type: PreviousOwner
        """
        if self.local_vars_configuration.client_side_validation and previous_owner is None:  # noqa: E501
            raise ValueError("Invalid value for `previous_owner`, must not be `None`")  # noqa: E501

        self._previous_owner = previous_owner

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
        if not isinstance(other, SalesContract):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SalesContract):
            return True

        return self.to_dict() != other.to_dict()
