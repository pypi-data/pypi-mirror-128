import logging
import os
import functools
import tempfile
import json
from typing import Tuple, Type, Optional
from enum import Enum
from bson import ObjectId
from datetime import datetime

import pandas as pd
from flask import Response, has_request_context, make_response, request, send_from_directory

from ...basic.dt.utils import DATETIME_FMT_FULL
from ...basic.error.utils import S_OK, E_INTERNAL, RobertError
from ...basic.validation import input
from ...basic.log import utils as logutils


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime(DATETIME_FMT_FULL)
        elif str(obj).lower() == 'nan':
            return None
        elif isinstance(obj, pd.Series):
            return obj.to_json(orient='values')
        elif isinstance(obj, pd.DataFrame):
            return obj.to_json(orient='records')
        elif isinstance(obj, Enum):
            return obj.value
        else:
            return obj


def robert_response(is_success, data, code, msg='') -> Response:
    if not code:
        code = S_OK if is_success else E_INTERNAL
    return Response(
        json.dumps({
            'success': is_success,
            'code': code,
            'data': data,
            'msg': msg
        }, cls=Encoder, ensure_ascii=False),
        mimetype='application/json')


def robert_response_error(data=None, code='0', msg='') -> Response:
    if isinstance(data, Exception):
        logging.error(data)
        data = str(data)
    return robert_response(False, data, code, msg)


def robert_response_success(data=None, code='1') -> Response:
    return robert_response(True, data, code)


ErrorTypes = Tuple[Type[Exception], ...]


def _get_error_response(e: Exception, user_errors: ErrorTypes) -> Response:
    is_robert_error = isinstance(e, RobertError)
    is_user_error = user_errors and isinstance(e, user_errors) or is_robert_error

    msg = getattr(e, 'msg', e.__str__())
    data = dict(error_type=str(type(e)),
                detail=getattr(e, 'data', getattr(e, 'detail', None)))

    if is_user_error:
        code = getattr(e, 'code', E_INTERNAL)
        logging.error(e.__str__())
    else:
        code = E_INTERNAL
        data['inner_code'] = getattr(e, 'code', None)
        # noinspection PyUnusedLocal
        url = request.url or 'N/A'
        logutils.log_unhandled_error()
    return robert_response_error(code=code, msg=msg, data=data)


def response_wrapper(func, tolerable_errors: Optional[ErrorTypes] = None):
    tolerable_errors = input.ensure_tuple_of(
        'tolerable_errors', tolerable_errors, (input.ensure_not_none_of, Type))

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Response:
        try:
            if has_request_context() and 'doc' in request.args:
                rv = make_response(func.__doc__)
                rv.headers['Content-Type'] = 'plain/text'
                return rv
            else:
                rv = func(*args, **kwargs)
                return robert_response_success(data=rv)
        except Exception as e:
            return _get_error_response(e, tolerable_errors)

    return wrapper


def file_response_wrapper(func, tolerable_errors: Optional[ErrorTypes] = None):
    tolerable_errors = input.ensure_tuple_of(
        'tolerable_errors', tolerable_errors, (input.ensure_not_none_of, Type))

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Response:
        try:
            file_path = func(*args, **kwargs)
            return send_from_directory(path=file_path, directory=os.path.dirname(file_path), filename=os.path.basename(file_path), as_attachment=True, attachment_filename=os.path.basename(file_path))
        except Exception as e:
            return _get_error_response(e, tolerable_errors)

    return wrapper
