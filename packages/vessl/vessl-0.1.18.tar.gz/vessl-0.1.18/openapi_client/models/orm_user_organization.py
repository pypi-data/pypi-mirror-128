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


class OrmUserOrganization(object):
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
        'created_dt': 'datetime',
        'edges': 'OrmUserOrganizationEdges',
        'id': 'int',
        'immutable_slug': 'str',
        'permission': 'str',
        'updated_dt': 'datetime',
        'user_organization_organization': 'int',
        'user_organization_user': 'int'
    }

    attribute_map = {
        'created_dt': 'created_dt',
        'edges': 'edges',
        'id': 'id',
        'immutable_slug': 'immutable_slug',
        'permission': 'permission',
        'updated_dt': 'updated_dt',
        'user_organization_organization': 'user_organization_organization',
        'user_organization_user': 'user_organization_user'
    }

    def __init__(self, created_dt=None, edges=None, id=None, immutable_slug=None, permission=None, updated_dt=None, user_organization_organization=None, user_organization_user=None, local_vars_configuration=None):  # noqa: E501
        """OrmUserOrganization - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._created_dt = None
        self._edges = None
        self._id = None
        self._immutable_slug = None
        self._permission = None
        self._updated_dt = None
        self._user_organization_organization = None
        self._user_organization_user = None
        self.discriminator = None

        if created_dt is not None:
            self.created_dt = created_dt
        if edges is not None:
            self.edges = edges
        if id is not None:
            self.id = id
        if immutable_slug is not None:
            self.immutable_slug = immutable_slug
        if permission is not None:
            self.permission = permission
        if updated_dt is not None:
            self.updated_dt = updated_dt
        if user_organization_organization is not None:
            self.user_organization_organization = user_organization_organization
        if user_organization_user is not None:
            self.user_organization_user = user_organization_user

    @property
    def created_dt(self):
        """Gets the created_dt of this OrmUserOrganization.  # noqa: E501


        :return: The created_dt of this OrmUserOrganization.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this OrmUserOrganization.


        :param created_dt: The created_dt of this OrmUserOrganization.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def edges(self):
        """Gets the edges of this OrmUserOrganization.  # noqa: E501


        :return: The edges of this OrmUserOrganization.  # noqa: E501
        :rtype: OrmUserOrganizationEdges
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this OrmUserOrganization.


        :param edges: The edges of this OrmUserOrganization.  # noqa: E501
        :type edges: OrmUserOrganizationEdges
        """

        self._edges = edges

    @property
    def id(self):
        """Gets the id of this OrmUserOrganization.  # noqa: E501


        :return: The id of this OrmUserOrganization.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OrmUserOrganization.


        :param id: The id of this OrmUserOrganization.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def immutable_slug(self):
        """Gets the immutable_slug of this OrmUserOrganization.  # noqa: E501


        :return: The immutable_slug of this OrmUserOrganization.  # noqa: E501
        :rtype: str
        """
        return self._immutable_slug

    @immutable_slug.setter
    def immutable_slug(self, immutable_slug):
        """Sets the immutable_slug of this OrmUserOrganization.


        :param immutable_slug: The immutable_slug of this OrmUserOrganization.  # noqa: E501
        :type immutable_slug: str
        """

        self._immutable_slug = immutable_slug

    @property
    def permission(self):
        """Gets the permission of this OrmUserOrganization.  # noqa: E501


        :return: The permission of this OrmUserOrganization.  # noqa: E501
        :rtype: str
        """
        return self._permission

    @permission.setter
    def permission(self, permission):
        """Sets the permission of this OrmUserOrganization.


        :param permission: The permission of this OrmUserOrganization.  # noqa: E501
        :type permission: str
        """

        self._permission = permission

    @property
    def updated_dt(self):
        """Gets the updated_dt of this OrmUserOrganization.  # noqa: E501


        :return: The updated_dt of this OrmUserOrganization.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this OrmUserOrganization.


        :param updated_dt: The updated_dt of this OrmUserOrganization.  # noqa: E501
        :type updated_dt: datetime
        """

        self._updated_dt = updated_dt

    @property
    def user_organization_organization(self):
        """Gets the user_organization_organization of this OrmUserOrganization.  # noqa: E501


        :return: The user_organization_organization of this OrmUserOrganization.  # noqa: E501
        :rtype: int
        """
        return self._user_organization_organization

    @user_organization_organization.setter
    def user_organization_organization(self, user_organization_organization):
        """Sets the user_organization_organization of this OrmUserOrganization.


        :param user_organization_organization: The user_organization_organization of this OrmUserOrganization.  # noqa: E501
        :type user_organization_organization: int
        """

        self._user_organization_organization = user_organization_organization

    @property
    def user_organization_user(self):
        """Gets the user_organization_user of this OrmUserOrganization.  # noqa: E501


        :return: The user_organization_user of this OrmUserOrganization.  # noqa: E501
        :rtype: int
        """
        return self._user_organization_user

    @user_organization_user.setter
    def user_organization_user(self, user_organization_user):
        """Sets the user_organization_user of this OrmUserOrganization.


        :param user_organization_user: The user_organization_user of this OrmUserOrganization.  # noqa: E501
        :type user_organization_user: int
        """

        self._user_organization_user = user_organization_user

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
        if not isinstance(other, OrmUserOrganization):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrmUserOrganization):
            return True

        return self.to_dict() != other.to_dict()
