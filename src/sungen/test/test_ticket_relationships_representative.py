# coding: utf-8

"""
    Open API Specification

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.ticket_relationships_representative import TicketRelationshipsRepresentative

class TestTicketRelationshipsRepresentative(unittest.TestCase):
    """TicketRelationshipsRepresentative unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TicketRelationshipsRepresentative:
        """Test TicketRelationshipsRepresentative
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TicketRelationshipsRepresentative`
        """
        model = TicketRelationshipsRepresentative()
        if include_optional:
            return TicketRelationshipsRepresentative(
                data = [
                    openapi_client.models.ticket_relationships_representative_data_inner.ticket_relationships_representative_data_inner(
                        id = '', 
                        meta = { }, 
                        type = '', )
                    ]
            )
        else:
            return TicketRelationshipsRepresentative(
        )
        """

    def testTicketRelationshipsRepresentative(self):
        """Test TicketRelationshipsRepresentative"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
