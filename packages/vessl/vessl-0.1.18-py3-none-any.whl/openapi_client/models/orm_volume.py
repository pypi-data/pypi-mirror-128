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


class OrmVolume(object):
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
        'base_path': 'str',
        'bucket_name': 'str',
        'created_dt': 'datetime',
        'edges': 'OrmVolumeEdges',
        'file_count': 'int',
        'id': 'int',
        'immutable_slug': 'str',
        'is_read_only': 'bool',
        'last_sync_time': 'datetime',
        'local_volume_config': 'dict(str, object)',
        'role_owner_ref': 'int',
        'role_type': 'str',
        'size': 'int',
        'status': 'str',
        'updated_dt': 'datetime',
        'volume_organization': 'int',
        'volume_storage': 'int'
    }

    attribute_map = {
        'base_path': 'base_path',
        'bucket_name': 'bucket_name',
        'created_dt': 'created_dt',
        'edges': 'edges',
        'file_count': 'file_count',
        'id': 'id',
        'immutable_slug': 'immutable_slug',
        'is_read_only': 'is_read_only',
        'last_sync_time': 'last_sync_time',
        'local_volume_config': 'local_volume_config',
        'role_owner_ref': 'role_owner_ref',
        'role_type': 'role_type',
        'size': 'size',
        'status': 'status',
        'updated_dt': 'updated_dt',
        'volume_organization': 'volume_organization',
        'volume_storage': 'volume_storage'
    }

    def __init__(self, base_path=None, bucket_name=None, created_dt=None, edges=None, file_count=None, id=None, immutable_slug=None, is_read_only=None, last_sync_time=None, local_volume_config=None, role_owner_ref=None, role_type=None, size=None, status=None, updated_dt=None, volume_organization=None, volume_storage=None, local_vars_configuration=None):  # noqa: E501
        """OrmVolume - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._base_path = None
        self._bucket_name = None
        self._created_dt = None
        self._edges = None
        self._file_count = None
        self._id = None
        self._immutable_slug = None
        self._is_read_only = None
        self._last_sync_time = None
        self._local_volume_config = None
        self._role_owner_ref = None
        self._role_type = None
        self._size = None
        self._status = None
        self._updated_dt = None
        self._volume_organization = None
        self._volume_storage = None
        self.discriminator = None

        if base_path is not None:
            self.base_path = base_path
        self.bucket_name = bucket_name
        if created_dt is not None:
            self.created_dt = created_dt
        if edges is not None:
            self.edges = edges
        if file_count is not None:
            self.file_count = file_count
        if id is not None:
            self.id = id
        if immutable_slug is not None:
            self.immutable_slug = immutable_slug
        if is_read_only is not None:
            self.is_read_only = is_read_only
        self.last_sync_time = last_sync_time
        if local_volume_config is not None:
            self.local_volume_config = local_volume_config
        if role_owner_ref is not None:
            self.role_owner_ref = role_owner_ref
        if role_type is not None:
            self.role_type = role_type
        if size is not None:
            self.size = size
        if status is not None:
            self.status = status
        if updated_dt is not None:
            self.updated_dt = updated_dt
        if volume_organization is not None:
            self.volume_organization = volume_organization
        if volume_storage is not None:
            self.volume_storage = volume_storage

    @property
    def base_path(self):
        """Gets the base_path of this OrmVolume.  # noqa: E501


        :return: The base_path of this OrmVolume.  # noqa: E501
        :rtype: str
        """
        return self._base_path

    @base_path.setter
    def base_path(self, base_path):
        """Sets the base_path of this OrmVolume.


        :param base_path: The base_path of this OrmVolume.  # noqa: E501
        :type base_path: str
        """

        self._base_path = base_path

    @property
    def bucket_name(self):
        """Gets the bucket_name of this OrmVolume.  # noqa: E501


        :return: The bucket_name of this OrmVolume.  # noqa: E501
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """Sets the bucket_name of this OrmVolume.


        :param bucket_name: The bucket_name of this OrmVolume.  # noqa: E501
        :type bucket_name: str
        """

        self._bucket_name = bucket_name

    @property
    def created_dt(self):
        """Gets the created_dt of this OrmVolume.  # noqa: E501


        :return: The created_dt of this OrmVolume.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this OrmVolume.


        :param created_dt: The created_dt of this OrmVolume.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def edges(self):
        """Gets the edges of this OrmVolume.  # noqa: E501


        :return: The edges of this OrmVolume.  # noqa: E501
        :rtype: OrmVolumeEdges
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this OrmVolume.


        :param edges: The edges of this OrmVolume.  # noqa: E501
        :type edges: OrmVolumeEdges
        """

        self._edges = edges

    @property
    def file_count(self):
        """Gets the file_count of this OrmVolume.  # noqa: E501


        :return: The file_count of this OrmVolume.  # noqa: E501
        :rtype: int
        """
        return self._file_count

    @file_count.setter
    def file_count(self, file_count):
        """Sets the file_count of this OrmVolume.


        :param file_count: The file_count of this OrmVolume.  # noqa: E501
        :type file_count: int
        """

        self._file_count = file_count

    @property
    def id(self):
        """Gets the id of this OrmVolume.  # noqa: E501


        :return: The id of this OrmVolume.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OrmVolume.


        :param id: The id of this OrmVolume.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def immutable_slug(self):
        """Gets the immutable_slug of this OrmVolume.  # noqa: E501


        :return: The immutable_slug of this OrmVolume.  # noqa: E501
        :rtype: str
        """
        return self._immutable_slug

    @immutable_slug.setter
    def immutable_slug(self, immutable_slug):
        """Sets the immutable_slug of this OrmVolume.


        :param immutable_slug: The immutable_slug of this OrmVolume.  # noqa: E501
        :type immutable_slug: str
        """

        self._immutable_slug = immutable_slug

    @property
    def is_read_only(self):
        """Gets the is_read_only of this OrmVolume.  # noqa: E501


        :return: The is_read_only of this OrmVolume.  # noqa: E501
        :rtype: bool
        """
        return self._is_read_only

    @is_read_only.setter
    def is_read_only(self, is_read_only):
        """Sets the is_read_only of this OrmVolume.


        :param is_read_only: The is_read_only of this OrmVolume.  # noqa: E501
        :type is_read_only: bool
        """

        self._is_read_only = is_read_only

    @property
    def last_sync_time(self):
        """Gets the last_sync_time of this OrmVolume.  # noqa: E501


        :return: The last_sync_time of this OrmVolume.  # noqa: E501
        :rtype: datetime
        """
        return self._last_sync_time

    @last_sync_time.setter
    def last_sync_time(self, last_sync_time):
        """Sets the last_sync_time of this OrmVolume.


        :param last_sync_time: The last_sync_time of this OrmVolume.  # noqa: E501
        :type last_sync_time: datetime
        """

        self._last_sync_time = last_sync_time

    @property
    def local_volume_config(self):
        """Gets the local_volume_config of this OrmVolume.  # noqa: E501


        :return: The local_volume_config of this OrmVolume.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._local_volume_config

    @local_volume_config.setter
    def local_volume_config(self, local_volume_config):
        """Sets the local_volume_config of this OrmVolume.


        :param local_volume_config: The local_volume_config of this OrmVolume.  # noqa: E501
        :type local_volume_config: dict(str, object)
        """

        self._local_volume_config = local_volume_config

    @property
    def role_owner_ref(self):
        """Gets the role_owner_ref of this OrmVolume.  # noqa: E501


        :return: The role_owner_ref of this OrmVolume.  # noqa: E501
        :rtype: int
        """
        return self._role_owner_ref

    @role_owner_ref.setter
    def role_owner_ref(self, role_owner_ref):
        """Sets the role_owner_ref of this OrmVolume.


        :param role_owner_ref: The role_owner_ref of this OrmVolume.  # noqa: E501
        :type role_owner_ref: int
        """

        self._role_owner_ref = role_owner_ref

    @property
    def role_type(self):
        """Gets the role_type of this OrmVolume.  # noqa: E501


        :return: The role_type of this OrmVolume.  # noqa: E501
        :rtype: str
        """
        return self._role_type

    @role_type.setter
    def role_type(self, role_type):
        """Sets the role_type of this OrmVolume.


        :param role_type: The role_type of this OrmVolume.  # noqa: E501
        :type role_type: str
        """

        self._role_type = role_type

    @property
    def size(self):
        """Gets the size of this OrmVolume.  # noqa: E501


        :return: The size of this OrmVolume.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this OrmVolume.


        :param size: The size of this OrmVolume.  # noqa: E501
        :type size: int
        """

        self._size = size

    @property
    def status(self):
        """Gets the status of this OrmVolume.  # noqa: E501


        :return: The status of this OrmVolume.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this OrmVolume.


        :param status: The status of this OrmVolume.  # noqa: E501
        :type status: str
        """

        self._status = status

    @property
    def updated_dt(self):
        """Gets the updated_dt of this OrmVolume.  # noqa: E501


        :return: The updated_dt of this OrmVolume.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this OrmVolume.


        :param updated_dt: The updated_dt of this OrmVolume.  # noqa: E501
        :type updated_dt: datetime
        """

        self._updated_dt = updated_dt

    @property
    def volume_organization(self):
        """Gets the volume_organization of this OrmVolume.  # noqa: E501


        :return: The volume_organization of this OrmVolume.  # noqa: E501
        :rtype: int
        """
        return self._volume_organization

    @volume_organization.setter
    def volume_organization(self, volume_organization):
        """Sets the volume_organization of this OrmVolume.


        :param volume_organization: The volume_organization of this OrmVolume.  # noqa: E501
        :type volume_organization: int
        """

        self._volume_organization = volume_organization

    @property
    def volume_storage(self):
        """Gets the volume_storage of this OrmVolume.  # noqa: E501


        :return: The volume_storage of this OrmVolume.  # noqa: E501
        :rtype: int
        """
        return self._volume_storage

    @volume_storage.setter
    def volume_storage(self, volume_storage):
        """Sets the volume_storage of this OrmVolume.


        :param volume_storage: The volume_storage of this OrmVolume.  # noqa: E501
        :type volume_storage: int
        """

        self._volume_storage = volume_storage

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
        if not isinstance(other, OrmVolume):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrmVolume):
            return True

        return self.to_dict() != other.to_dict()
