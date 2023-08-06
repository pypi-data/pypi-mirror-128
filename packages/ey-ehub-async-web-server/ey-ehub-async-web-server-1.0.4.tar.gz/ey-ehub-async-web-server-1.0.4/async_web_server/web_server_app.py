import os
from http import HTTPStatus
from typing import Dict, Callable
from flask import Flask, jsonify, request
from utils.async_web_server.request_scheduler import (EHubAsynchronousServiceRequestScheduler,
                                                      RequestState)
from utils.async_web_server.request_arguments_adapter import (RequestArgumentsAdapter,
                                                              NoopRequestArgumentsAdapter)


class EHubAsynchronousWebServerApp(Flask):

    REQUEST_STATE_2_HTTP_CODE = {
        RequestState.UNKNOWN          : HTTPStatus.NOT_FOUND,
        RequestState.SUBMITTED        : HTTPStatus.CREATED,
        RequestState.IN_PROGRESS      : HTTPStatus.ACCEPTED,
        RequestState.PROCESSING_ERROR : HTTPStatus.INTERNAL_SERVER_ERROR,
        RequestState.COMPLETED        : HTTPStatus.OK,
    }

    def __init__(self):
        super().__init__(__name__)
        self._request_scheduler = None

    def initialize(self,
                   request_name_2_handler_mapping: Dict[str, Callable],
                   request_args_adapter: RequestArgumentsAdapter = NoopRequestArgumentsAdapter(),
                   *args,
                   **kwargs):
        self._request_scheduler = EHubAsynchronousServiceRequestScheduler(
                                    request_name_2_handler_mapping,
                                    request_args_adapter,
                                    *args, **kwargs)
        self._request_scheduler.initialize()

    def submit_request(self, request_name: str, request_args=(), request_kwargs={}):
        status, msg = self._request_scheduler.submit_request(request_name,
                                                             request_args,
                                                             request_kwargs)
        return msg, self.translate_request_status_2_http_code(status)

    def get_request_state(self, request_id: str):
        status, msg = self._request_scheduler.get_request_state(request_id)
        return msg, self.translate_request_status_2_http_code(status)

    def translate_request_status_2_http_code(self, request_status: RequestState):
        return self.REQUEST_STATE_2_HTTP_CODE[request_status]


WEB_APP = EHubAsynchronousWebServerApp()


@WEB_APP.route('/')
def health_check():
    '''Sample health check
    '''
    service, version = (os.getenv('SERVICE_NAME', '<unknown>'),
                        os.getenv('SERVICE_VERSION', '<unknown>'),)
    return jsonify({'serviceName': str(service),
                    'version': str(version),
                    'status': 'up'})


@WEB_APP.route('/submit-request', methods=['POST'])
def submit_request():
    ''' Universal endpoint for submitting a request
    '''
    return WEB_APP.submit_request(request.json['function'],
                                  request_kwargs=request.json.get('call_args', {}))


@WEB_APP.route('/get-request-state/<string:request_id>', methods=['GET'])
def get_request_state(request_id):
    ''' Universal endpoint for retrieving request state
    '''
    return WEB_APP.get_request_state(request_id)
