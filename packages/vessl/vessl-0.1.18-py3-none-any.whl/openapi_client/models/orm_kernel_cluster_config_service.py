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


class OrmKernelClusterConfigService(object):
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
        'annotations': 'dict(str, str)',
        'http_annotations': 'dict(str, str)',
        'labels': 'dict(str, str)',
        'tcp_annotations': 'dict(str, str)'
    }

    attribute_map = {
        'annotations': 'annotations',
        'http_annotations': 'http_annotations',
        'labels': 'labels',
        'tcp_annotations': 'tcp_annotations'
    }

    def __init__(self, annotations=None, http_annotations=None, labels=None, tcp_annotations=None, local_vars_configuration=None):  # noqa: E501
        """OrmKernelClusterConfigService - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._annotations = None
        self._http_annotations = None
        self._labels = None
        self._tcp_annotations = None
        self.discriminator = None

        if annotations is not None:
            self.annotations = annotations
        if http_annotations is not None:
            self.http_annotations = http_annotations
        if labels is not None:
            self.labels = labels
        if tcp_annotations is not None:
            self.tcp_annotations = tcp_annotations

    @property
    def annotations(self):
        """Gets the annotations of this OrmKernelClusterConfigService.  # noqa: E501


        :return: The annotations of this OrmKernelClusterConfigService.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._annotations

    @annotations.setter
    def annotations(self, annotations):
        """Sets the annotations of this OrmKernelClusterConfigService.


        :param annotations: The annotations of this OrmKernelClusterConfigService.  # noqa: E501
        :type annotations: dict(str, str)
        """

        self._annotations = annotations

    @property
    def http_annotations(self):
        """Gets the http_annotations of this OrmKernelClusterConfigService.  # noqa: E501


        :return: The http_annotations of this OrmKernelClusterConfigService.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._http_annotations

    @http_annotations.setter
    def http_annotations(self, http_annotations):
        """Sets the http_annotations of this OrmKernelClusterConfigService.


        :param http_annotations: The http_annotations of this OrmKernelClusterConfigService.  # noqa: E501
        :type http_annotations: dict(str, str)
        """

        self._http_annotations = http_annotations

    @property
    def labels(self):
        """Gets the labels of this OrmKernelClusterConfigService.  # noqa: E501


        :return: The labels of this OrmKernelClusterConfigService.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this OrmKernelClusterConfigService.


        :param labels: The labels of this OrmKernelClusterConfigService.  # noqa: E501
        :type labels: dict(str, str)
        """

        self._labels = labels

    @property
    def tcp_annotations(self):
        """Gets the tcp_annotations of this OrmKernelClusterConfigService.  # noqa: E501


        :return: The tcp_annotations of this OrmKernelClusterConfigService.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._tcp_annotations

    @tcp_annotations.setter
    def tcp_annotations(self, tcp_annotations):
        """Sets the tcp_annotations of this OrmKernelClusterConfigService.


        :param tcp_annotations: The tcp_annotations of this OrmKernelClusterConfigService.  # noqa: E501
        :type tcp_annotations: dict(str, str)
        """

        self._tcp_annotations = tcp_annotations

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
        if not isinstance(other, OrmKernelClusterConfigService):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrmKernelClusterConfigService):
            return True

        return self.to_dict() != other.to_dict()
