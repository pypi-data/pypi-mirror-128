from .consts import *

class Account():

    def __init__(self, client):
        self._client = client

    def get_account(self) -> dict:
        '''Get information about your account.'''
        
        params: RequestParams = {
            'method': HTTPMethod.GET,
            'path': '/account',
            'body': None,
            'req_content_type': ContentType.JSON,
            'res_content_type': ContentType.JSON
        }

        return self._client._make_request(params)
