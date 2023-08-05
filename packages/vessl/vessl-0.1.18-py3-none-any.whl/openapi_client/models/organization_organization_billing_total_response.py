# coding: utf-8

"""
    Aron API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


import inspect
import pprint
import re  # noqa: F401
import six

from openapi_client.configuration import Configuration


class OrganizationOrganizationBillingTotalResponse(object):
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
        'credit_balance': 'float',
        'total': 'float',
        'upcoming_payment': 'float'
    }

    attribute_map = {
        'credit_balance': 'credit_balance',
        'total': 'total',
        'upcoming_payment': 'upcoming_payment'
    }

    def __init__(self, credit_balance=None, total=None, upcoming_payment=None, local_vars_configuration=None):  # noqa: E501
        """OrganizationOrganizationBillingTotalResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._credit_balance = None
        self._total = None
        self._upcoming_payment = None
        self.discriminator = None

        self.credit_balance = credit_balance
        self.total = total
        self.upcoming_payment = upcoming_payment

    @property
    def credit_balance(self):
        """Gets the credit_balance of this OrganizationOrganizationBillingTotalResponse.  # noqa: E501


        :return: The credit_balance of this OrganizationOrganizationBillingTotalResponse.  # noqa: E501
        :rtype: float
        """
        return self._credit_balance

    @credit_balance.setter
    def credit_balance(self, credit_balance):
        """Sets the credit_balance of this OrganizationOrganizationBillingTotalResponse.


        :param credit_balance: The credit_balance of this OrganizationOrganizationBillingTotalResponse.  # noqa: E501
        :type credit_balance: float
        """
        if self.local_vars_configuration.client_side_validation and credit_balance is None:  # noqa: E501
            raise ValueError("Invalid value for `credit_balance`, must not be `None`")  # noqa: E501

        self._credit_balance = credit_balance

    @property
    def total(self):
        """Gets the total of this OrganizationOrganizationBillingTotalResponse.  # noqa: E501


        :return: The total of this OrganizationOrganizationBillingTotalResponse.  # noqa: E501
        :rtype: float
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this OrganizationOrganizationBillingTotalResponse.


        :param total: The total of this OrganizationOrganizationBillingTotalResponse.  # noqa: E501
        :type total: float
        """
        if self.local_vars_configuration.client_side_validation and total is None:  # noqa: E501
            raise ValueError("Invalid value for `total`, must not be `None`")  # noqa: E501

        self._total = total

    @property
    def upcoming_payment(self):
        """Gets the upcoming_payment of this OrganizationOrganizationBillingTotalResponse.  # noqa: E501


        :return: The upcoming_payment of this OrganizationOrganizationBillingTotalResponse.  # noqa: E501
        :rtype: float
        """
        return self._upcoming_payment

    @upcoming_payment.setter
    def upcoming_payment(self, upcoming_payment):
        """Sets the upcoming_payment of this OrganizationOrganizationBillingTotalResponse.


        :param upcoming_payment: The upcoming_payment of this OrganizationOrganizationBillingTotalResponse.  # noqa: E501
        :type upcoming_payment: float
        """
        if self.local_vars_configuration.client_side_validation and upcoming_payment is None:  # noqa: E501
            raise ValueError("Invalid value for `upcoming_payment`, must not be `None`")  # noqa: E501

        self._upcoming_payment = upcoming_payment

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = inspect.getargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OrganizationOrganizationBillingTotalResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrganizationOrganizationBillingTotalResponse):
            return True

        return self.to_dict() != other.to_dict()
