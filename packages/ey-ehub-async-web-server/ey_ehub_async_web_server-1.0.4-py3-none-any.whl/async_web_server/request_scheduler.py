import time
import uuid
import logging
import threading
from datetime import datetime
from enum import Enum
from typing import Tuple, Dict, Any, Callable
from utils.async_web_server.request_arguments_adapter import (RequestArgumentsAdapter,
                                                              NoopRequestArgumentsAdapter)


class RequestState(Enum):
    UNKNOWN          = -1
    SUBMITTED        =  0
    IN_PROGRESS      =  1
    PROCESSING_ERROR =  2
    COMPLETED        =  3


class Request(object):

    ALLOWED_STATE_TRANSITIONS = {
        RequestState.UNKNOWN: [RequestState.UNKNOWN],
        RequestState.SUBMITTED: [RequestState.IN_PROGRESS],
        RequestState.IN_PROGRESS: [RequestState.PROCESSING_ERROR, RequestState.COMPLETED],
        RequestState.PROCESSING_ERROR: [RequestState.PROCESSING_ERROR],
        RequestState.COMPLETED: [RequestState.COMPLETED]
    }

    FINAL_STATES = [RequestState.UNKNOWN,
                    RequestState.PROCESSING_ERROR,
                    RequestState.COMPLETED]

    def __init__(self, name: str, call_args: Tuple, call_kwargs: Dict[str, Any]):
        self.name = name
        self.args = call_args
        self.kwargs = call_kwargs
        self._set_new_state(RequestState.SUBMITTED, '')

    @classmethod
    def is_request_final_state(cls, state: RequestState):
        return state in cls.FINAL_STATES

    def change_state(self, state: RequestState, msg: str = ''):
        if self._is_allowed_state_transition(state):
            self._set_new_state(state, msg)
        else:
            exception_msg = ('Unsupported state transition requested from '
                             f'{self.state} to {state}')
            logging.error(exception_msg)
            raise Exception(exception_msg)

    def _is_allowed_state_transition(self, state):
        return state in self.ALLOWED_STATE_TRANSITIONS

    def _set_new_state(self, state, msg):
        self.state = state
        self.msg = msg if msg else ''
        self.last_modified_ts = datetime.utcnow()


class EHubAsynchronousServiceRequestScheduler(object):

    MARK_AS_OBSOLETE_REQUEST_TIMEOUT = 30 # in minutes
    REQUEST_PROCESSING_STEP = 2 # in seconds

    def __init__(self,
                 request_name_2_handler: Dict[str, Callable],
                 request_args_adapter: RequestArgumentsAdapter = NoopRequestArgumentsAdapter(),
                 mark_as_obsolete_request_timeout: int = MARK_AS_OBSOLETE_REQUEST_TIMEOUT,
                 request_processing_step: int = REQUEST_PROCESSING_STEP):
        self._request_name_2_handler = request_name_2_handler
        self._request_args_adapter = request_args_adapter
        self._mark_as_obsolete_request_timeout = mark_as_obsolete_request_timeout
        self._request_processing_step = request_processing_step
        self._request_2_status = {}
        self._pending_requests = []
        self._processing_loop_thread = None

    def get_request_state(self, request_id: str):
        try:
            request = self._request_2_status[request_id]
            return request.state, request.msg
        except KeyError:
            return RequestState.UNKNOWN, ''

    def initialize(self):
        self._processing_loop_thread = threading.Thread(target=self.run_processing_loop)
        self._processing_loop_thread.setDaemon(True)
        self._processing_loop_thread.start()

    def process_requests(self):
        while len(self._pending_requests) > 0:
            request_id = self._pending_requests.pop(0)
            self._process_request(request_id)
        self._request_dustbin_collector()

    def run_processing_loop(self):
        while True:
            self.process_requests()
            time.sleep(self._request_processing_step)

    def submit_request(self,
                       request_name:str,
                       request_args: Tuple=(),
                       request_kwargs: Dict[str, Any]={}):
        logging.info(f'Submit request: {request_name} with '
                      f'args: {request_args} and kwargs: {request_kwargs}')
        error_code, msg = (RequestState.UNKNOWN, 'Unsupported request name provided.')
        if self._is_supported_request(request_name):
            error_code, msg = self._add_new_request(request_name,
                                                    request_args,
                                                    request_kwargs)
        else:
            logging.error(f'Trying to submit unsupported request: {request_name}')
        return error_code, msg

    def _is_supported_request(self, request_name):
        return request_name in self._request_name_2_handler.keys()

    def _add_new_request(self, request_name, request_args, request_kwargs):
        request_id = self._generate_request_id()
        request = Request(request_name, request_args, request_kwargs)
        self._request_2_status[request_id] = request
        self._pending_requests.append(request_id)
        return request.state, request_id

    def _process_request(self, request_id):
        try:
            self._try_to_process_request(request_id)
        except Exception as e:
            self._handle_request_processing_exception(request_id, e)

    def _request_dustbin_collector(self):
        for request_id in self._request_2_status.copy():
            if self._is_obsolete_request(request_id):
                logging.debug(f'Forget request with ID: {request_id}')
                del self._request_2_status[request_id]

    def _generate_request_id(self):
        return str(uuid.uuid4())

    def _try_to_process_request(self, request_id):
        request = self._request_2_status[request_id]
        logging.info(f'Start processing request with ID: {request_id} of type: {request.name}'
                     f' with args: {request.args} and kwargs: {request.kwargs}.'
                     f' {len(self._pending_requests)} request(s) pending...')
        request.change_state(RequestState.IN_PROGRESS)
        args, kwargs = self._request_args_adapter.adapt(*request.args, **request.kwargs)
        msg = self._request_name_2_handler[request.name](*args, **kwargs)
        request.change_state(RequestState.COMPLETED, msg)
        logging.info(f'Completed processing a request with ID: {request_id}')

    def _handle_request_processing_exception(self, request_id, e):
        request = self._request_2_status[request_id]
        logging.exception(f'Could not process a request with ID: {request_id}. '
                          f'Exception has been thrown: {e}')
        request.change_state(RequestState.PROCESSING_ERROR,
                             (f'Exception thrown while handling the request: {e}. '
                               'Check service logs for details'))

    def _is_obsolete_request(self, request_id):
        request = self._request_2_status[request_id]
        return (Request.is_request_final_state(request.state)
                and self._does_obsolete_timeout_expired(request.last_modified_ts))

    def _does_obsolete_timeout_expired(self, timestamp):
        return (((datetime.utcnow() - timestamp).total_seconds()/60) >=
                self._mark_as_obsolete_request_timeout)
