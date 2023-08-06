import numpy as np
from PIL import Image
import io
from .exceptions import RequestException, InvalidArgsException
from .consts import *

class Maps():

    def __init__(self, client):
        self._client = client

    def create_map(self, slug: str, name: str, description: str = None) -> dict:
        '''Creates a new map.'''

        body = {
            'slug' : slug,
            'name': name,
        }
        
        if description:
            body['description'] = description

        params: RequestParams = {
            'method': HTTPMethod.POST,
            'path': '/maps',
            'body': body,
            'req_content_type': ContentType.JSON,
            'res_content_type': ContentType.JSON
        }

        return self._client._make_request(params)

    def list_maps(self) -> dict:
        '''Lists maps.'''
        
        params: RequestParams = {
            'method': HTTPMethod.GET,
            'path': '/maps',
            'body': None,
            'req_content_type': ContentType.JSON,
            'res_content_type': ContentType.JSON
        }

        return self._client._make_request(params)

    def get_map_metadata(self, slug: str) -> dict:
        '''Get metadata about a map.'''
        
        params: RequestParams = {
            'method': HTTPMethod.GET,
            'path': f'/maps/{slug}',
            'body': None,
            'req_content_type': ContentType.JSON,
            'res_content_type': ContentType.JSON
        }

        return self._client._make_request(params)

    def update_map_metadata(self, slug: str, name: str = None, description: str = None) -> dict:
        '''Updates metadata about a map.'''

        # user must specify name or description
        if not name and not description:
            raise InvalidArgsException('You must specify a name or description')

        body = {}
        
        if name:
            body['name'] = name

        if description:
            body['description'] = description
        
        params: RequestParams = {
            'method': HTTPMethod.PATCH,
            'path': f'/maps/{slug}',
            'body': body,
            'req_content_type': ContentType.JSON,
            'res_content_type': ContentType.JSON
        }

        return self._client._make_request(params)

    def delete_map(self, slug: str) -> dict:
        '''Delete a map.'''
        
        params: RequestParams = {
            'method': HTTPMethod.DELETE,
            'path': f'/maps/{slug}',
            'body': None,
            'req_content_type': ContentType.JSON,
            'res_content_type': ContentType.JSON
        }

        return self._client._make_request(params)

    def delete_map_versions(self, slug: str) -> dict:
        '''Deletes all versions of the map but does not delete the map itself.'''
        
        params: RequestParams = {
            'method': HTTPMethod.DELETE,
            'path': f'/maps/{slug}/versions',
            'body': None,
            'req_content_type': ContentType.JSON,
            'res_content_type': ContentType.JSON
        }

        return self._client._make_request(params)

    def upload_map(self, slug: str, map_array: 'np.ndarray[np.uint8]') -> dict:
        '''Uploads a 2d array of map data to a map.'''

        # Construct Pgm buffer from 2d array
        buf = io.BytesIO()
        img = Image.fromarray(map_array , 'L')
        img.save(buf, format='PPM')
        buf.seek(0)
        
        params: RequestParams = {
            'method': HTTPMethod.POST,
            'path': f'/maps/{slug}/ingest',
            'body': buf,
            'req_content_type': ContentType.PGM,
            'res_content_type': ContentType.JSON
        }

        return self._client._make_request(params)

    def upload_map_from_file(self, slug: str, filepath: str = './map.pgm') -> dict:
        '''Reads from a file and uploads the data to a map.'''

        # Will raise FileNotFoundError if the file cannot be found
        with open(filepath, 'rb') as fh:
            data = fh.read()
            
            params: RequestParams = {
                'method': HTTPMethod.POST,
                'path': f'/maps/{slug}/ingest',
                'body': data,
                'req_content_type': ContentType.PGM,
                'res_content_type': ContentType.JSON
            }

            return self._client._make_request(params)

    def download_map(self, slug: str, version: str = 'latest') -> 'np.ndarray[np.uint8]':
        '''Downloads data from a map and returns as a 2d array.'''

        params: RequestParams = {
            'method': HTTPMethod.GET,
            'path': f'/maps/{slug}/{version}/egest',
            'body': None,
            'req_content_type': ContentType.JSON,
            'res_content_type': ContentType.PGM
        }

        response = self._client._make_request(params)
        print('got it')

        return self._parse_pgm(response)

    def download_map_to_file(self, slug: str, version: str = 'latest', filepath: str = './map.pgm') -> None:
        '''Downloads data from a map and writes it to a file.'''

        params: RequestParams = {
            'method': HTTPMethod.GET,
            'path': f'/maps/{slug}/{version}/egest',
            'body': None,
            'req_content_type': ContentType.JSON,
            'res_content_type': ContentType.PGM
        }

        response = self._client._make_request(params)

        with open(filepath, 'wb') as f:
            f.write(response)


    # Helper functions
    
    def _parse_pgm(self, buffer):
        '''Helper function to read and parse PGM images from the server.'''

        # First two chars should contain the codec
        codec = buffer[0:2].decode('ascii')

        if codec == PgmCodec.P2:
            return self._parse_p2_pgm(buffer)

        elif codec == PgmCodec.P5:
            img = Image.open(io.BytesIO(buffer)) # formats=('PPM',)
            arr = np.asarray(img, 'uint8')
            return arr.reshape((img.height, img.width))

        else:
            # Cannot parse pgm codec
            raise RequestException

    def _parse_p2_pgm(self, buffer) -> 'np.ndarray[np.uint8]':
        '''Helper function to parse a P2 PGM.
        
        PIL does not support the P2 ascii format so we roll our own parser.'''

        def read_noncomment_lines(lines):
            # reads lines from file, will skip over comments
            this_line = lines.pop().decode('ascii')
            while this_line[0] == '#':
                this_line = lines.pop().decode('ascii')
            return this_line

        buff = io.BytesIO(buffer)

        lines = buff.readlines()
        lines.reverse()

        read_noncomment_lines(lines) # codec
        dims = read_noncomment_lines(lines).split(' ') # width height
        width = int(dims[0])
        height = int(dims[1])
        read_noncomment_lines(lines) # max value

        arr = []
        while len(lines) > 0:
            row = read_noncomment_lines(lines)
            arr.append([int(c) for c in row.split()])

        arr = np.array(arr, 'uint8')
        return arr.reshape((height, width))