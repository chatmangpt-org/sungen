# coding: utf-8

"""
    Open API Specification

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.tickets_post_request import TicketsPostRequest

class TestTicketsPostRequest(unittest.TestCase):
    """TicketsPostRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TicketsPostRequest:
        """Test TicketsPostRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TicketsPostRequest`
        """
        model = TicketsPostRequest()
        if include_optional:
            return TicketsPostRequest(
                data = openapi_client.models._tickets_post_request_data._tickets_post_request_data(
                    attributes = openapi_client.models._tickets_post_request_data_attributes._tickets_post_request_data_attributes(
                        subject = '', ), 
                    relationships = openapi_client.models.relationships.relationships(), 
                    type = 'ticket', )
            )
        else:
            return TicketsPostRequest(
                data = openapi_client.models._tickets_post_request_data._tickets_post_request_data(
                    attributes = openapi_client.models._tickets_post_request_data_attributes._tickets_post_request_data_attributes(
                        subject = '', ), 
                    relationships = openapi_client.models.relationships.relationships(), 
                    type = 'ticket', ),
        )
        """

    def testTicketsPostRequest(self):
        """Test TicketsPostRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
