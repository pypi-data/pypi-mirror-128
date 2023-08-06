from .consts import *

class ApiKeys():

    def __init__(self, client):
        self._client = client

    def create_api_key(self) -> dict:
        '''Create an API key.'''
        
        params: RequestParams = {
            'method': HTTPMethod.POST,
            'path': '/api-keys',
            'body': None,
            'req_content_type': ContentType.JSON,
            'res_content_type': ContentType.JSON
        }

        return self._client._make_request(params)

    def list_api_keys(self) -> dict:
        '''Lists API keys in your account.'''
        
        params: RequestParams = {
            'method': HTTPMethod.GET,
            'path': '/api-keys',
            'body': None,
            'req_content_type': ContentType.JSON,
            'res_content_type': ContentType.JSON
        }

        return self._client._make_request(params)

    def delete_api_key(self, key_id: str) -> dict:
        '''Delete API key.'''
        
        params: RequestParams = {
            'method': HTTPMethod.DELETE,
            'path': f'/api-keys/{key_id}',
            'body': None,
            'req_content_type': ContentType.JSON,
            'res_content_type': ContentType.JSON
        }

        return self._client._make_request(params)
