# coding: utf-8

"""
    Open API Specification

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.ticket_attributes import TicketAttributes

class TestTicketAttributes(unittest.TestCase):
    """TicketAttributes unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TicketAttributes:
        """Test TicketAttributes
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TicketAttributes`
        """
        model = TicketAttributes()
        if include_optional:
            return TicketAttributes(
                representative_id = '',
                subject = ''
            )
        else:
            return TicketAttributes(
                subject = '',
        )
        """

    def testTicketAttributes(self):
        """Test TicketAttributes"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
