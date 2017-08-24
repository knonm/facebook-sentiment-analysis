import requests
import hashlib
import json
import base64
import ast
from pathlib import Path

api_host = 'graph.facebook.com'
api_version = 'v2.9'
api_URL = 'https://%s/%s' % (api_host, api_version)

class HTTPError(Exception):
    def __init__(self, method, urlReq, req_response):
        self.method = method
        self.urlReq = urlReq
        self.req_response = req_response
        
    def __str__(self):
        sep = '===================================================='
        return '\n%s\nMethod: %s\nURL: %s\nResponse Code: %d\n\nResponse Header:\n%s\n\nResponse:\n%s\n%s\n' % (sep, self.method, 
        self.urlReq, self.req_response.status_code, self.req_response.headers, self.req_response.text, sep)

    def get_facebook_error(self):
        res = json.loads(self.req_response.text)
        return '%s' % (res['error']['type'])
        

class HTTPTooManyError(HTTPError):
    pass

def get_API(endpoint, end_params, token):
    if end_params == None:
        endpoint_URL = '%s/%s' % (api_URL, endpoint)
    else:
        endpoint_URL = '%s/%s?%s&access_token=%s' % (api_URL, endpoint, end_params, token)
    
    req_response = requests.get(endpoint_URL,
        headers = { 'host':api_host,
                    'accept':'application/json',
                    'accept-encoding':'UTF-8'})
    
    if req_response.status_code == requests.codes.ok:
        return req_response.json()
    elif req_response.status_code == requests.codes.too_many:
        raise HTTPTooManyError('get_API', endpoint_URL, req_response)
    else:
        raise HTTPError('get_API', endpoint_URL, req_response)

def get_token():
    token_URL = '%s/oauth/access_token' % (api_URL)
    file_fb_auth = open('facebook_auth.txt', 'r')
    client_id = file_fb_auth.readline().replace('\n', '')
    client_secret = file_fb_auth.readline().replace('\n', '')
    file_fb_auth.close()
    grant_type = 'client_credentials'
    
    get_params = { 'client_id':client_id,
                   'client_secret':client_secret,
                   'grant_type':grant_type }
    
    req_response = requests.get(token_URL, params=get_params)
    
    if req_response.status_code == requests.codes.ok:
        return req_response.json()['access_token']
    elif req_response.status_code == requests.codes.too_many:
        raise HTTPTooManyError('get_token', token_URL, req_response)
    else:
        raise HTTPError('get_token', token_URL, req_response)

def request_API(endpoint, end_params):
    json_file_name = hashlib.md5(('%s%s' % (endpoint, end_params)).encode('utf-8')).hexdigest()
    json_file = Path('./cache/facebook/%s.json' % (json_file_name))
    json_content = None
    if json_file.is_file():
        json_content = json_file.read_text(encoding='utf-8')
        json_content = json.loads(json_content)
    else:
        token = get_token()
        json_content = get_API(endpoint, end_params, token)
        json_file.write_text(json.dumps(json_content), encoding='utf-8')
    return json_content
