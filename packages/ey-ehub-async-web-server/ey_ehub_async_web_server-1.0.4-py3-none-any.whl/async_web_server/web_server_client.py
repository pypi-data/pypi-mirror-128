import time
import logging
import requests
import msal
from http import HTTPStatus


class EhubRequest(object):

    def __init__(self, authenticator=None):
        self._authenticator = authenticator
        self._token = self._generate_token()

    def get(self, url, **kwargs):
        return self._send_request(requests.get, url, kwargs)

    def post(self, url, **kwargs):
        return self._send_request(requests.post, url, kwargs)

    def _send_request(self, req_fun, url, req_kwargs):
        response = req_fun(url, **self._build_request_kwargs(req_kwargs))
        if self._authenticator and response.status_code == HTTPStatus.UNAUTHORIZED:
            self._generate_token()
            response = req_fun(url, **self._build_request_kwargs(req_kwargs))
        return response

    def _build_request_kwargs(self, custom_req_kwargs):
        if self._token:
            return {**custom_req_kwargs, **self._get_authentication_header()}
        else:
            return custom_req_kwargs

    def _generate_token(self):
        if self._authenticator:
            self._token = self._authenticator.get_auth_token()

    def _get_authentication_header(self):
        return {'headers': {'Authorization': self._token}} if self._authenticator else {}


class AzureClientAuthorizer(object):

    _DEFAULT_AZURE_AUTHORITY_MAIN_URL = 'https://login.microsoftonline.com'
    _AZURE_SCOPE_TEMPLATE = 'api://{client_id}/.default'

    def __init__(self,
                 client_id,
                 client_secret,
                 tenant_id,
                 authority_main_url=_DEFAULT_AZURE_AUTHORITY_MAIN_URL):
        self._client_id, self._client_secret = (client_id, client_secret)
        self._authority_url = f'{authority_main_url}/{tenant_id}'

    def get_auth_token(self):
        token_data = (self._get_confidential_client_app()
                      .acquire_token_for_client(scopes=self._get_scopes()))
        return f'{token_data["token_type"]} {token_data["access_token"]}'

    def _get_confidential_client_app(self):
        return msal.ConfidentialClientApplication(self._client_id,
                                                  authority=self._authority_url,
                                                  client_credential=self._client_secret)

    def _get_scopes(self):
        return [self._AZURE_SCOPE_TEMPLATE.format(client_id=self._client_id)]


class EHubWebServerClient(object):

    DEFAULT_WEB_SERVER_URL = 'http://127.0.0.1'
    DEFAULT_WEB_SERVER_PORT = 5000


class EHubWebServerAsynchronousClient(EHubWebServerClient):

    _SUBMIT_REQUEST_ENDPOINT = 'submit-request'
    _GET_REQUEST_STATE_ENDPOINT = 'get-request-state'

    def __init__(self,
                 server_url=EHubWebServerClient.DEFAULT_WEB_SERVER_URL,
                 server_port=EHubWebServerClient.DEFAULT_WEB_SERVER_PORT,
                 authorizer=None):
        self._endpoint = server_url + (f':{server_port}' if server_port else '')
        self._token = None
        self._requestor = EhubRequest(authorizer)

    def submit_request(self, function_name, **function_call_args):
        logging.debug(f'Submit request: "{function_name}", call args: {function_call_args}')
        return self._requestor.post(f'{self._endpoint}/{self._SUBMIT_REQUEST_ENDPOINT}',
                             json={'function': function_name, 'call_args': function_call_args})

    def get_request_state(self, request_id):
        logging.debug(f'Get request state for request ID: {request_id}')
        return self._requestor.get(f'{self._endpoint}/{self._GET_REQUEST_STATE_ENDPOINT}/{request_id}')


class EHubWebServerSynchronousClient(EHubWebServerClient):

    POLLING_STATE_FREQUENCY = 2 # in seconds

    _REQUEST_FINAL_STATES = [HTTPStatus.OK,
                             HTTPStatus.NOT_FOUND,
                             HTTPStatus.INTERNAL_SERVER_ERROR]

    def __init__(self,
                 server_url=EHubWebServerClient.DEFAULT_WEB_SERVER_URL,
                 server_port=EHubWebServerClient.DEFAULT_WEB_SERVER_PORT,
                 authorizer=None,
                 request_polling_freq=POLLING_STATE_FREQUENCY):
        self._async_client = EHubWebServerAsynchronousClient(server_url,
                                                             server_port,
                                                             authorizer)
        self._request_polling_freq = request_polling_freq

    def call(self, function_name, **kwargs):
        logging.info(f'Call server function name: "{function_name}", call args: {kwargs}')
        response = self._async_client.submit_request(function_name, **kwargs)
        if response.status_code == HTTPStatus.CREATED:
            return self._poll_request_until_handled(response.text)
        logging.info(f'Return response with status code: {response.status_code}'
                     f' and text: "{response.text}"')
        return response

    def _poll_request_until_handled(self, request_id):
        while True:
           response = self._async_client.get_request_state(request_id)
           if response.status_code in self._REQUEST_FINAL_STATES:
               return response
           time.sleep(self._request_polling_freq)
