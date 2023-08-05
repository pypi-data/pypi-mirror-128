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


class ResponseDashboardResponse(object):
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
        'chart_fields': 'list[ResponseDashboardChartField]',
        'chart_sections': 'list[ResponseDashboardChartSection]',
        'filters': 'list[ResponseDashboardExperimentFilterResponse]',
        'sorts': 'list[ResponseDashboardExperimentSortResponse]'
    }

    attribute_map = {
        'chart_fields': 'chart_fields',
        'chart_sections': 'chart_sections',
        'filters': 'filters',
        'sorts': 'sorts'
    }

    def __init__(self, chart_fields=None, chart_sections=None, filters=None, sorts=None, local_vars_configuration=None):  # noqa: E501
        """ResponseDashboardResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._chart_fields = None
        self._chart_sections = None
        self._filters = None
        self._sorts = None
        self.discriminator = None

        self.chart_fields = chart_fields
        self.chart_sections = chart_sections
        self.filters = filters
        self.sorts = sorts

    @property
    def chart_fields(self):
        """Gets the chart_fields of this ResponseDashboardResponse.  # noqa: E501


        :return: The chart_fields of this ResponseDashboardResponse.  # noqa: E501
        :rtype: list[ResponseDashboardChartField]
        """
        return self._chart_fields

    @chart_fields.setter
    def chart_fields(self, chart_fields):
        """Sets the chart_fields of this ResponseDashboardResponse.


        :param chart_fields: The chart_fields of this ResponseDashboardResponse.  # noqa: E501
        :type chart_fields: list[ResponseDashboardChartField]
        """
        if self.local_vars_configuration.client_side_validation and chart_fields is None:  # noqa: E501
            raise ValueError("Invalid value for `chart_fields`, must not be `None`")  # noqa: E501

        self._chart_fields = chart_fields

    @property
    def chart_sections(self):
        """Gets the chart_sections of this ResponseDashboardResponse.  # noqa: E501


        :return: The chart_sections of this ResponseDashboardResponse.  # noqa: E501
        :rtype: list[ResponseDashboardChartSection]
        """
        return self._chart_sections

    @chart_sections.setter
    def chart_sections(self, chart_sections):
        """Sets the chart_sections of this ResponseDashboardResponse.


        :param chart_sections: The chart_sections of this ResponseDashboardResponse.  # noqa: E501
        :type chart_sections: list[ResponseDashboardChartSection]
        """
        if self.local_vars_configuration.client_side_validation and chart_sections is None:  # noqa: E501
            raise ValueError("Invalid value for `chart_sections`, must not be `None`")  # noqa: E501

        self._chart_sections = chart_sections

    @property
    def filters(self):
        """Gets the filters of this ResponseDashboardResponse.  # noqa: E501


        :return: The filters of this ResponseDashboardResponse.  # noqa: E501
        :rtype: list[ResponseDashboardExperimentFilterResponse]
        """
        return self._filters

    @filters.setter
    def filters(self, filters):
        """Sets the filters of this ResponseDashboardResponse.


        :param filters: The filters of this ResponseDashboardResponse.  # noqa: E501
        :type filters: list[ResponseDashboardExperimentFilterResponse]
        """
        if self.local_vars_configuration.client_side_validation and filters is None:  # noqa: E501
            raise ValueError("Invalid value for `filters`, must not be `None`")  # noqa: E501

        self._filters = filters

    @property
    def sorts(self):
        """Gets the sorts of this ResponseDashboardResponse.  # noqa: E501


        :return: The sorts of this ResponseDashboardResponse.  # noqa: E501
        :rtype: list[ResponseDashboardExperimentSortResponse]
        """
        return self._sorts

    @sorts.setter
    def sorts(self, sorts):
        """Sets the sorts of this ResponseDashboardResponse.


        :param sorts: The sorts of this ResponseDashboardResponse.  # noqa: E501
        :type sorts: list[ResponseDashboardExperimentSortResponse]
        """
        if self.local_vars_configuration.client_side_validation and sorts is None:  # noqa: E501
            raise ValueError("Invalid value for `sorts`, must not be `None`")  # noqa: E501

        self._sorts = sorts

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
        if not isinstance(other, ResponseDashboardResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponseDashboardResponse):
            return True

        return self.to_dict() != other.to_dict()
