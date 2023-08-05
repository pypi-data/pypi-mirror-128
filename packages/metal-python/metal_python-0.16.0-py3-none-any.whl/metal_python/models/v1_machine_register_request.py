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


class V1MachineRegisterRequest(object):
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
        'bios': 'V1MachineBIOS',
        'hardware': 'V1MachineHardwareExtended',
        'ipmi': 'V1MachineIPMI',
        'partitionid': 'str',
        'rackid': 'str',
        'tags': 'list[str]',
        'uuid': 'str'
    }

    attribute_map = {
        'bios': 'bios',
        'hardware': 'hardware',
        'ipmi': 'ipmi',
        'partitionid': 'partitionid',
        'rackid': 'rackid',
        'tags': 'tags',
        'uuid': 'uuid'
    }

    def __init__(self, bios=None, hardware=None, ipmi=None, partitionid=None, rackid=None, tags=None, uuid=None):  # noqa: E501
        """V1MachineRegisterRequest - a model defined in Swagger"""  # noqa: E501

        self._bios = None
        self._hardware = None
        self._ipmi = None
        self._partitionid = None
        self._rackid = None
        self._tags = None
        self._uuid = None
        self.discriminator = None

        self.bios = bios
        self.hardware = hardware
        self.ipmi = ipmi
        self.partitionid = partitionid
        self.rackid = rackid
        self.tags = tags
        self.uuid = uuid

    @property
    def bios(self):
        """Gets the bios of this V1MachineRegisterRequest.  # noqa: E501

        bios information of this machine  # noqa: E501

        :return: The bios of this V1MachineRegisterRequest.  # noqa: E501
        :rtype: V1MachineBIOS
        """
        return self._bios

    @bios.setter
    def bios(self, bios):
        """Sets the bios of this V1MachineRegisterRequest.

        bios information of this machine  # noqa: E501

        :param bios: The bios of this V1MachineRegisterRequest.  # noqa: E501
        :type: V1MachineBIOS
        """
        if bios is None:
            raise ValueError("Invalid value for `bios`, must not be `None`")  # noqa: E501

        self._bios = bios

    @property
    def hardware(self):
        """Gets the hardware of this V1MachineRegisterRequest.  # noqa: E501

        the hardware of this machine  # noqa: E501

        :return: The hardware of this V1MachineRegisterRequest.  # noqa: E501
        :rtype: V1MachineHardwareExtended
        """
        return self._hardware

    @hardware.setter
    def hardware(self, hardware):
        """Sets the hardware of this V1MachineRegisterRequest.

        the hardware of this machine  # noqa: E501

        :param hardware: The hardware of this V1MachineRegisterRequest.  # noqa: E501
        :type: V1MachineHardwareExtended
        """
        if hardware is None:
            raise ValueError("Invalid value for `hardware`, must not be `None`")  # noqa: E501

        self._hardware = hardware

    @property
    def ipmi(self):
        """Gets the ipmi of this V1MachineRegisterRequest.  # noqa: E501

        the ipmi access infos  # noqa: E501

        :return: The ipmi of this V1MachineRegisterRequest.  # noqa: E501
        :rtype: V1MachineIPMI
        """
        return self._ipmi

    @ipmi.setter
    def ipmi(self, ipmi):
        """Sets the ipmi of this V1MachineRegisterRequest.

        the ipmi access infos  # noqa: E501

        :param ipmi: The ipmi of this V1MachineRegisterRequest.  # noqa: E501
        :type: V1MachineIPMI
        """
        if ipmi is None:
            raise ValueError("Invalid value for `ipmi`, must not be `None`")  # noqa: E501

        self._ipmi = ipmi

    @property
    def partitionid(self):
        """Gets the partitionid of this V1MachineRegisterRequest.  # noqa: E501

        the partition id to register this machine with  # noqa: E501

        :return: The partitionid of this V1MachineRegisterRequest.  # noqa: E501
        :rtype: str
        """
        return self._partitionid

    @partitionid.setter
    def partitionid(self, partitionid):
        """Sets the partitionid of this V1MachineRegisterRequest.

        the partition id to register this machine with  # noqa: E501

        :param partitionid: The partitionid of this V1MachineRegisterRequest.  # noqa: E501
        :type: str
        """
        if partitionid is None:
            raise ValueError("Invalid value for `partitionid`, must not be `None`")  # noqa: E501

        self._partitionid = partitionid

    @property
    def rackid(self):
        """Gets the rackid of this V1MachineRegisterRequest.  # noqa: E501

        the rack id where this machine is connected to  # noqa: E501

        :return: The rackid of this V1MachineRegisterRequest.  # noqa: E501
        :rtype: str
        """
        return self._rackid

    @rackid.setter
    def rackid(self, rackid):
        """Sets the rackid of this V1MachineRegisterRequest.

        the rack id where this machine is connected to  # noqa: E501

        :param rackid: The rackid of this V1MachineRegisterRequest.  # noqa: E501
        :type: str
        """
        if rackid is None:
            raise ValueError("Invalid value for `rackid`, must not be `None`")  # noqa: E501

        self._rackid = rackid

    @property
    def tags(self):
        """Gets the tags of this V1MachineRegisterRequest.  # noqa: E501

        tags for this machine  # noqa: E501

        :return: The tags of this V1MachineRegisterRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this V1MachineRegisterRequest.

        tags for this machine  # noqa: E501

        :param tags: The tags of this V1MachineRegisterRequest.  # noqa: E501
        :type: list[str]
        """
        if tags is None:
            raise ValueError("Invalid value for `tags`, must not be `None`")  # noqa: E501

        self._tags = tags

    @property
    def uuid(self):
        """Gets the uuid of this V1MachineRegisterRequest.  # noqa: E501

        the product uuid of the machine to register  # noqa: E501

        :return: The uuid of this V1MachineRegisterRequest.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this V1MachineRegisterRequest.

        the product uuid of the machine to register  # noqa: E501

        :param uuid: The uuid of this V1MachineRegisterRequest.  # noqa: E501
        :type: str
        """
        if uuid is None:
            raise ValueError("Invalid value for `uuid`, must not be `None`")  # noqa: E501

        self._uuid = uuid

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
        if issubclass(V1MachineRegisterRequest, dict):
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
        if not isinstance(other, V1MachineRegisterRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
