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


class V1FilesystemLayoutConstraints(object):
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
        'images': 'dict(str, str)',
        'sizes': 'list[str]'
    }

    attribute_map = {
        'images': 'images',
        'sizes': 'sizes'
    }

    def __init__(self, images=None, sizes=None):  # noqa: E501
        """V1FilesystemLayoutConstraints - a model defined in Swagger"""  # noqa: E501

        self._images = None
        self._sizes = None
        self.discriminator = None

        self.images = images
        if sizes is not None:
            self.sizes = sizes

    @property
    def images(self):
        """Gets the images of this V1FilesystemLayoutConstraints.  # noqa: E501

        list of images this layout applies to  # noqa: E501

        :return: The images of this V1FilesystemLayoutConstraints.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._images

    @images.setter
    def images(self, images):
        """Sets the images of this V1FilesystemLayoutConstraints.

        list of images this layout applies to  # noqa: E501

        :param images: The images of this V1FilesystemLayoutConstraints.  # noqa: E501
        :type: dict(str, str)
        """
        if images is None:
            raise ValueError("Invalid value for `images`, must not be `None`")  # noqa: E501

        self._images = images

    @property
    def sizes(self):
        """Gets the sizes of this V1FilesystemLayoutConstraints.  # noqa: E501

        list of sizes this layout applies to  # noqa: E501

        :return: The sizes of this V1FilesystemLayoutConstraints.  # noqa: E501
        :rtype: list[str]
        """
        return self._sizes

    @sizes.setter
    def sizes(self, sizes):
        """Sets the sizes of this V1FilesystemLayoutConstraints.

        list of sizes this layout applies to  # noqa: E501

        :param sizes: The sizes of this V1FilesystemLayoutConstraints.  # noqa: E501
        :type: list[str]
        """

        self._sizes = sizes

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
        if issubclass(V1FilesystemLayoutConstraints, dict):
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
        if not isinstance(other, V1FilesystemLayoutConstraints):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
