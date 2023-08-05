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


class V1SwitchUpdateRequest(object):
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
        'description': 'str',
        'id': 'str',
        'mode': 'str',
        'name': 'str',
        'rack_id': 'str'
    }

    attribute_map = {
        'description': 'description',
        'id': 'id',
        'mode': 'mode',
        'name': 'name',
        'rack_id': 'rack_id'
    }

    def __init__(self, description=None, id=None, mode=None, name=None, rack_id=None):  # noqa: E501
        """V1SwitchUpdateRequest - a model defined in Swagger"""  # noqa: E501

        self._description = None
        self._id = None
        self._mode = None
        self._name = None
        self._rack_id = None
        self.discriminator = None

        if description is not None:
            self.description = description
        self.id = id
        if mode is not None:
            self.mode = mode
        if name is not None:
            self.name = name
        self.rack_id = rack_id

    @property
    def description(self):
        """Gets the description of this V1SwitchUpdateRequest.  # noqa: E501

        a description for this entity  # noqa: E501

        :return: The description of this V1SwitchUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this V1SwitchUpdateRequest.

        a description for this entity  # noqa: E501

        :param description: The description of this V1SwitchUpdateRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def id(self):
        """Gets the id of this V1SwitchUpdateRequest.  # noqa: E501

        the unique ID of this entity  # noqa: E501

        :return: The id of this V1SwitchUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this V1SwitchUpdateRequest.

        the unique ID of this entity  # noqa: E501

        :param id: The id of this V1SwitchUpdateRequest.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def mode(self):
        """Gets the mode of this V1SwitchUpdateRequest.  # noqa: E501

        the mode the switch currently has  # noqa: E501

        :return: The mode of this V1SwitchUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """Sets the mode of this V1SwitchUpdateRequest.

        the mode the switch currently has  # noqa: E501

        :param mode: The mode of this V1SwitchUpdateRequest.  # noqa: E501
        :type: str
        """

        self._mode = mode

    @property
    def name(self):
        """Gets the name of this V1SwitchUpdateRequest.  # noqa: E501

        a readable name for this entity  # noqa: E501

        :return: The name of this V1SwitchUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this V1SwitchUpdateRequest.

        a readable name for this entity  # noqa: E501

        :param name: The name of this V1SwitchUpdateRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def rack_id(self):
        """Gets the rack_id of this V1SwitchUpdateRequest.  # noqa: E501

        the id of the rack in which this switch is located  # noqa: E501

        :return: The rack_id of this V1SwitchUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._rack_id

    @rack_id.setter
    def rack_id(self, rack_id):
        """Sets the rack_id of this V1SwitchUpdateRequest.

        the id of the rack in which this switch is located  # noqa: E501

        :param rack_id: The rack_id of this V1SwitchUpdateRequest.  # noqa: E501
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
        if issubclass(V1SwitchUpdateRequest, dict):
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
        if not isinstance(other, V1SwitchUpdateRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
