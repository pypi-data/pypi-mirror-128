# coding: utf-8

"""
    metal-api

    API to manage and control plane resources like machines, switches, operating system images, machine sizes, networks, IP addresses and more  # noqa: E501

    OpenAPI spec version: v0.16.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class V1SwitchResponse(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'changed': 'datetime',
        'connections': 'list[V1SwitchConnection]',
        'created': 'datetime',
        'description': 'str',
        'id': 'str',
        'last_sync': 'V1SwitchSync',
        'last_sync_error': 'V1SwitchSync',
        'mode': 'str',
        'name': 'str',
        'nics': 'list[V1SwitchNic]',
        'partition': 'V1PartitionResponse',
        'rack_id': 'str'
    }

    attribute_map = {
        'changed': 'changed',
        'connections': 'connections',
        'created': 'created',
        'description': 'description',
        'id': 'id',
        'last_sync': 'last_sync',
        'last_sync_error': 'last_sync_error',
        'mode': 'mode',
        'name': 'name',
        'nics': 'nics',
        'partition': 'partition',
        'rack_id': 'rack_id'
    }

    def __init__(self, changed=None, connections=None, created=None, description=None, id=None, last_sync=None, last_sync_error=None, mode=None, name=None, nics=None, partition=None, rack_id=None):  # noqa: E501
        """V1SwitchResponse - a model defined in Swagger"""  # noqa: E501

        self._changed = None
        self._connections = None
        self._created = None
        self._description = None
        self._id = None
        self._last_sync = None
        self._last_sync_error = None
        self._mode = None
        self._name = None
        self._nics = None
        self._partition = None
        self._rack_id = None
        self.discriminator = None

        if changed is not None:
            self.changed = changed
        self.connections = connections
        if created is not None:
            self.created = created
        if description is not None:
            self.description = description
        self.id = id
        if last_sync is not None:
            self.last_sync = last_sync
        if last_sync_error is not None:
            self.last_sync_error = last_sync_error
        if mode is not None:
            self.mode = mode
        if name is not None:
            self.name = name
        self.nics = nics
        self.partition = partition
        self.rack_id = rack_id

    @property
    def changed(self):
        """Gets the changed of this V1SwitchResponse.  # noqa: E501

        the last changed timestamp of this entity  # noqa: E501

        :return: The changed of this V1SwitchResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._changed

    @changed.setter
    def changed(self, changed):
        """Sets the changed of this V1SwitchResponse.

        the last changed timestamp of this entity  # noqa: E501

        :param changed: The changed of this V1SwitchResponse.  # noqa: E501
        :type: datetime
        """

        self._changed = changed

    @property
    def connections(self):
        """Gets the connections of this V1SwitchResponse.  # noqa: E501

        a connection between a switch port and a machine  # noqa: E501

        :return: The connections of this V1SwitchResponse.  # noqa: E501
        :rtype: list[V1SwitchConnection]
        """
        return self._connections

    @connections.setter
    def connections(self, connections):
        """Sets the connections of this V1SwitchResponse.

        a connection between a switch port and a machine  # noqa: E501

        :param connections: The connections of this V1SwitchResponse.  # noqa: E501
        :type: list[V1SwitchConnection]
        """
        if connections is None:
            raise ValueError("Invalid value for `connections`, must not be `None`")  # noqa: E501

        self._connections = connections

    @property
    def created(self):
        """Gets the created of this V1SwitchResponse.  # noqa: E501

        the creation time of this entity  # noqa: E501

        :return: The created of this V1SwitchResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this V1SwitchResponse.

        the creation time of this entity  # noqa: E501

        :param created: The created of this V1SwitchResponse.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def description(self):
        """Gets the description of this V1SwitchResponse.  # noqa: E501

        a description for this entity  # noqa: E501

        :return: The description of this V1SwitchResponse.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this V1SwitchResponse.

        a description for this entity  # noqa: E501

        :param description: The description of this V1SwitchResponse.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def id(self):
        """Gets the id of this V1SwitchResponse.  # noqa: E501

        the unique ID of this entity  # noqa: E501

        :return: The id of this V1SwitchResponse.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this V1SwitchResponse.

        the unique ID of this entity  # noqa: E501

        :param id: The id of this V1SwitchResponse.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def last_sync(self):
        """Gets the last_sync of this V1SwitchResponse.  # noqa: E501

        last successful synchronization to the switch  # noqa: E501

        :return: The last_sync of this V1SwitchResponse.  # noqa: E501
        :rtype: V1SwitchSync
        """
        return self._last_sync

    @last_sync.setter
    def last_sync(self, last_sync):
        """Sets the last_sync of this V1SwitchResponse.

        last successful synchronization to the switch  # noqa: E501

        :param last_sync: The last_sync of this V1SwitchResponse.  # noqa: E501
        :type: V1SwitchSync
        """

        self._last_sync = last_sync

    @property
    def last_sync_error(self):
        """Gets the last_sync_error of this V1SwitchResponse.  # noqa: E501

        last synchronization to the switch that was erroneous  # noqa: E501

        :return: The last_sync_error of this V1SwitchResponse.  # noqa: E501
        :rtype: V1SwitchSync
        """
        return self._last_sync_error

    @last_sync_error.setter
    def last_sync_error(self, last_sync_error):
        """Sets the last_sync_error of this V1SwitchResponse.

        last synchronization to the switch that was erroneous  # noqa: E501

        :param last_sync_error: The last_sync_error of this V1SwitchResponse.  # noqa: E501
        :type: V1SwitchSync
        """

        self._last_sync_error = last_sync_error

    @property
    def mode(self):
        """Gets the mode of this V1SwitchResponse.  # noqa: E501

        the mode the switch currently has  # noqa: E501

        :return: The mode of this V1SwitchResponse.  # noqa: E501
        :rtype: str
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """Sets the mode of this V1SwitchResponse.

        the mode the switch currently has  # noqa: E501

        :param mode: The mode of this V1SwitchResponse.  # noqa: E501
        :type: str
        """

        self._mode = mode

    @property
    def name(self):
        """Gets the name of this V1SwitchResponse.  # noqa: E501

        a readable name for this entity  # noqa: E501

        :return: The name of this V1SwitchResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this V1SwitchResponse.

        a readable name for this entity  # noqa: E501

        :param name: The name of this V1SwitchResponse.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def nics(self):
        """Gets the nics of this V1SwitchResponse.  # noqa: E501

        the list of network interfaces on the switch  # noqa: E501

        :return: The nics of this V1SwitchResponse.  # noqa: E501
        :rtype: list[V1SwitchNic]
        """
        return self._nics

    @nics.setter
    def nics(self, nics):
        """Sets the nics of this V1SwitchResponse.

        the list of network interfaces on the switch  # noqa: E501

        :param nics: The nics of this V1SwitchResponse.  # noqa: E501
        :type: list[V1SwitchNic]
        """
        if nics is None:
            raise ValueError("Invalid value for `nics`, must not be `None`")  # noqa: E501

        self._nics = nics

    @property
    def partition(self):
        """Gets the partition of this V1SwitchResponse.  # noqa: E501

        the partition in which this switch is located  # noqa: E501

        :return: The partition of this V1SwitchResponse.  # noqa: E501
        :rtype: V1PartitionResponse
        """
        return self._partition

    @partition.setter
    def partition(self, partition):
        """Sets the partition of this V1SwitchResponse.

        the partition in which this switch is located  # noqa: E501

        :param partition: The partition of this V1SwitchResponse.  # noqa: E501
        :type: V1PartitionResponse
        """
        if partition is None:
            raise ValueError("Invalid value for `partition`, must not be `None`")  # noqa: E501

        self._partition = partition

    @property
    def rack_id(self):
        """Gets the rack_id of this V1SwitchResponse.  # noqa: E501

        the id of the rack in which this switch is located  # noqa: E501

        :return: The rack_id of this V1SwitchResponse.  # noqa: E501
        :rtype: str
        """
        return self._rack_id

    @rack_id.setter
    def rack_id(self, rack_id):
        """Sets the rack_id of this V1SwitchResponse.

        the id of the rack in which this switch is located  # noqa: E501

        :param rack_id: The rack_id of this V1SwitchResponse.  # noqa: E501
        :type: str
        """
        if rack_id is None:
            raise ValueError("Invalid value for `rack_id`, must not be `None`")  # noqa: E501

        self._rack_id = rack_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(V1SwitchResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1SwitchResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
