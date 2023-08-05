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


class ExperimentShowPlotsAPIPayload(object):
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
        'all': 'bool',
        'experiment_numbers': 'list[int]',
        'selected_only': 'bool'
    }

    attribute_map = {
        'all': 'all',
        'experiment_numbers': 'experiment_numbers',
        'selected_only': 'selected_only'
    }

    def __init__(self, all=None, experiment_numbers=None, selected_only=None, local_vars_configuration=None):  # noqa: E501
        """ExperimentShowPlotsAPIPayload - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._all = None
        self._experiment_numbers = None
        self._selected_only = None
        self.discriminator = None

        if all is not None:
            self.all = all
        if experiment_numbers is not None:
            self.experiment_numbers = experiment_numbers
        if selected_only is not None:
            self.selected_only = selected_only

    @property
    def all(self):
        """Gets the all of this ExperimentShowPlotsAPIPayload.  # noqa: E501


        :return: The all of this ExperimentShowPlotsAPIPayload.  # noqa: E501
        :rtype: bool
        """
        return self._all

    @all.setter
    def all(self, all):
        """Sets the all of this ExperimentShowPlotsAPIPayload.


        :param all: The all of this ExperimentShowPlotsAPIPayload.  # noqa: E501
        :type all: bool
        """

        self._all = all

    @property
    def experiment_numbers(self):
        """Gets the experiment_numbers of this ExperimentShowPlotsAPIPayload.  # noqa: E501


        :return: The experiment_numbers of this ExperimentShowPlotsAPIPayload.  # noqa: E501
        :rtype: list[int]
        """
        return self._experiment_numbers

    @experiment_numbers.setter
    def experiment_numbers(self, experiment_numbers):
        """Sets the experiment_numbers of this ExperimentShowPlotsAPIPayload.


        :param experiment_numbers: The experiment_numbers of this ExperimentShowPlotsAPIPayload.  # noqa: E501
        :type experiment_numbers: list[int]
        """

        self._experiment_numbers = experiment_numbers

    @property
    def selected_only(self):
        """Gets the selected_only of this ExperimentShowPlotsAPIPayload.  # noqa: E501


        :return: The selected_only of this ExperimentShowPlotsAPIPayload.  # noqa: E501
        :rtype: bool
        """
        return self._selected_only

    @selected_only.setter
    def selected_only(self, selected_only):
        """Sets the selected_only of this ExperimentShowPlotsAPIPayload.


        :param selected_only: The selected_only of this ExperimentShowPlotsAPIPayload.  # noqa: E501
        :type selected_only: bool
        """

        self._selected_only = selected_only

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
        if not isinstance(other, ExperimentShowPlotsAPIPayload):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ExperimentShowPlotsAPIPayload):
            return True

        return self.to_dict() != other.to_dict()
