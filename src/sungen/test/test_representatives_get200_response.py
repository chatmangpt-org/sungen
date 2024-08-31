# coding: utf-8

"""
    Open API Specification

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.representatives_get200_response import RepresentativesGet200Response

class TestRepresentativesGet200Response(unittest.TestCase):
    """RepresentativesGet200Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RepresentativesGet200Response:
        """Test RepresentativesGet200Response
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RepresentativesGet200Response`
        """
        model = RepresentativesGet200Response()
        if include_optional:
            return RepresentativesGet200Response(
                data = [
                    openapi_client.models.representative.representative(
                        attributes = openapi_client.models.representative_attributes.representative_attributes(
                            name = '', ), 
                        id = '', 
                        relationships = openapi_client.models.representative_relationships.representative_relationships(
                            tickets = openapi_client.models.representative_relationships_tickets.representative_relationships_tickets(
                                data = [
                                    openapi_client.models.representative_relationships_tickets_data_inner.representative_relationships_tickets_data_inner(
                                        id = '', 
                                        meta = { }, 
                                        type = '', )
                                    ], ), ), 
                        type = '', )
                    ],
                included = [
                    null
                    ],
                meta = { }
            )
        else:
            return RepresentativesGet200Response(
        )
        """

    def testRepresentativesGet200Response(self):
        """Test RepresentativesGet200Response"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
