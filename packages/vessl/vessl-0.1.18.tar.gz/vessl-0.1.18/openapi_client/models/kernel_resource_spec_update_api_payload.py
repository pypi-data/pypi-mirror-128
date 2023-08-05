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


class KernelResourceSpecUpdateAPIPayload(object):
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
        'description': 'str',
        'name': 'str',
        'priority': 'int'
    }

    attribute_map = {
        'description': 'description',
        'name': 'name',
        'priority': 'priority'
    }

    def __init__(self, description=None, name=None, priority=None, local_vars_configuration=None):  # noqa: E501
        """KernelResourceSpecUpdateAPIPayload - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._description = None
        self._name = None
        self._priority = None
        self.discriminator = None

        self.description = description
        self.name = name
        self.priority = priority

    @property
    def description(self):
        """Gets the description of this KernelResourceSpecUpdateAPIPayload.  # noqa: E501


        :return: The description of this KernelResourceSpecUpdateAPIPayload.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this KernelResourceSpecUpdateAPIPayload.


        :param description: The description of this KernelResourceSpecUpdateAPIPayload.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def name(self):
        """Gets the name of this KernelResourceSpecUpdateAPIPayload.  # noqa: E501


        :return: The name of this KernelResourceSpecUpdateAPIPayload.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this KernelResourceSpecUpdateAPIPayload.


        :param name: The name of this KernelResourceSpecUpdateAPIPayload.  # noqa: E501
        :type name: str
        """

        self._name = name

    @property
    def priority(self):
        """Gets the priority of this KernelResourceSpecUpdateAPIPayload.  # noqa: E501


        :return: The priority of this KernelResourceSpecUpdateAPIPayload.  # noqa: E501
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this KernelResourceSpecUpdateAPIPayload.


        :param priority: The priority of this KernelResourceSpecUpdateAPIPayload.  # noqa: E501
        :type priority: int
        """

        self._priority = priority

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
        if not isinstance(other, KernelResourceSpecUpdateAPIPayload):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, KernelResourceSpecUpdateAPIPayload):
            return True

        return self.to_dict() != other.to_dict()
