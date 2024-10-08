# openapi-client
No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

This Python package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 1.1
- Package version: 1.0.0
- Generator version: 7.7.0
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements.

Python 3.7+

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import openapi_client
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import openapi_client
```

### Tests

Execute `pytest` to run the tests.

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.RepresentativeApi(api_client)
    filter = openapi_client.RepresentativeFilter() # RepresentativeFilter | Filters the query to results with attributes matching the given filter object (optional)
    sort = 'sort_example' # str | Sort order to apply to the results (optional)
    page = openapi_client.RepresentativesGetPageParameter() # RepresentativesGetPageParameter | Paginates the response with the limit and offset or keyset pagination. (optional)
    include = 'include_example' # str | Relationship paths to include in the response (optional)
    fields = None # RepresentativesGetFieldsParameter | Limits the response fields to only those listed for each type (optional)

    try:
        api_response = api_instance.representatives_get(filter=filter, sort=sort, page=page, include=include, fields=fields)
        print("The response of RepresentativeApi->representatives_get:\n")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling RepresentativeApi->representatives_get: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*RepresentativeApi* | [**representatives_get**](docs/RepresentativeApi.md#representatives_get) | **GET** /representatives | 
*RepresentativeApi* | [**representatives_id_get**](docs/RepresentativeApi.md#representatives_id_get) | **GET** /representatives/{id} | 
*TicketApi* | [**tickets_get**](docs/TicketApi.md#tickets_get) | **GET** /tickets | 
*TicketApi* | [**tickets_id_get**](docs/TicketApi.md#tickets_id_get) | **GET** /tickets/{id} | 
*TicketApi* | [**tickets_id_patch**](docs/TicketApi.md#tickets_id_patch) | **PATCH** /tickets/{id} | 
*TicketApi* | [**tickets_post**](docs/TicketApi.md#tickets_post) | **POST** /tickets | 


## Documentation For Models

 - [Error](docs/Error.md)
 - [ErrorSource](docs/ErrorSource.md)
 - [Representative](docs/Representative.md)
 - [RepresentativeAttributes](docs/RepresentativeAttributes.md)
 - [RepresentativeFilter](docs/RepresentativeFilter.md)
 - [RepresentativeFilterId](docs/RepresentativeFilterId.md)
 - [RepresentativeFilterName](docs/RepresentativeFilterName.md)
 - [RepresentativeRelationships](docs/RepresentativeRelationships.md)
 - [RepresentativeRelationshipsTickets](docs/RepresentativeRelationshipsTickets.md)
 - [RepresentativeRelationshipsTicketsDataInner](docs/RepresentativeRelationshipsTicketsDataInner.md)
 - [RepresentativesGet200Response](docs/RepresentativesGet200Response.md)
 - [RepresentativesGetFieldsParameter](docs/RepresentativesGetFieldsParameter.md)
 - [RepresentativesGetPageParameter](docs/RepresentativesGetPageParameter.md)
 - [RepresentativesGetPageParameterAnyOf](docs/RepresentativesGetPageParameterAnyOf.md)
 - [RepresentativesGetPageParameterAnyOf1](docs/RepresentativesGetPageParameterAnyOf1.md)
 - [RepresentativesIdGet200Response](docs/RepresentativesIdGet200Response.md)
 - [Ticket](docs/Ticket.md)
 - [TicketAttributes](docs/TicketAttributes.md)
 - [TicketFilter](docs/TicketFilter.md)
 - [TicketFilterId](docs/TicketFilterId.md)
 - [TicketFilterRepresentativeId](docs/TicketFilterRepresentativeId.md)
 - [TicketFilterSubject](docs/TicketFilterSubject.md)
 - [TicketRelationships](docs/TicketRelationships.md)
 - [TicketRelationshipsRepresentative](docs/TicketRelationshipsRepresentative.md)
 - [TicketRelationshipsRepresentativeDataInner](docs/TicketRelationshipsRepresentativeDataInner.md)
 - [TicketsGet200Response](docs/TicketsGet200Response.md)
 - [TicketsGetFieldsParameter](docs/TicketsGetFieldsParameter.md)
 - [TicketsIdPatchRequest](docs/TicketsIdPatchRequest.md)
 - [TicketsIdPatchRequestData](docs/TicketsIdPatchRequestData.md)
 - [TicketsIdPatchRequestDataAttributes](docs/TicketsIdPatchRequestDataAttributes.md)
 - [TicketsPost201Response](docs/TicketsPost201Response.md)
 - [TicketsPostRequest](docs/TicketsPostRequest.md)
 - [TicketsPostRequestData](docs/TicketsPostRequestData.md)
 - [TicketsPostRequestDataAttributes](docs/TicketsPostRequestDataAttributes.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization


Authentication schemes defined for the API:
<a id="api_key"></a>
### api_key

- **Type**: API key
- **API key parameter name**: api_key
- **Location**: HTTP header


## Author




