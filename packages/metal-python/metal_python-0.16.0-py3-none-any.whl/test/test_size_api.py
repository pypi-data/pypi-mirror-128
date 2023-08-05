# coding: utf-8

"""
    metal-api

    API to manage and control plane resources like machines, switches, operating system images, machine sizes, networks, IP addresses and more  # noqa: E501

    OpenAPI spec version: v0.16.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import metal_python
from metal_python.api.size_api import SizeApi  # noqa: E501
from metal_python.rest import ApiException


class TestSizeApi(unittest.TestCase):
    """SizeApi unit test stubs"""

    def setUp(self):
        self.api = metal_python.api.size_api.SizeApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_size(self):
        """Test case for create_size

        create a size. if the given ID already exists a conflict is returned  # noqa: E501
        """
        pass

    def test_delete_size(self):
        """Test case for delete_size

        deletes an size and returns the deleted entity  # noqa: E501
        """
        pass

    def test_find_size(self):
        """Test case for find_size

        get size by id  # noqa: E501
        """
        pass

    def test_from_hardware(self):
        """Test case for from_hardware

        Searches all sizes for one to match the given hardwarespecs. If nothing is found, a list of entries is returned which describe the constraint which did not match  # noqa: E501
        """
        pass

    def test_list_sizes(self):
        """Test case for list_sizes

        get all sizes  # noqa: E501
        """
        pass

    def test_update_size(self):
        """Test case for update_size

        updates a size. if the size was changed since this one was read, a conflict is returned  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
