import json as json_
import typing

import aiohttp

from .exceptions import ApiException


def make_url(hostname: str, api_method: str, branch_id: int = 0) -> str:
    """
    Make url for api call
    :param hostname: hostname
    :param api_method: api method
    :param branch_id: branch id
    :return: full url
    """
    if branch_id:
        return f"https://{hostname}/v2api/{branch_id}/{api_method}"
    else:
        return f"https://{hostname}/v2api/{api_method}"


def check_response(
        code: int,
        body: str,
        request_info: typing.Optional[aiohttp.RequestInfo] = None
) -> typing.Dict[str, typing.Any]:
    """
    Check response
    :param code: response code
    :param request_info: request info
    :param body: response text
    :return: checked response
    """
    if code >= 500:
        raise ApiException(code, body, request_info)

    try:
        json_response = json_.loads(body)
    except ValueError:
        json_response = {}
    is_ok = True

    if 'errors' in json_response and json_response.get('errors'):
        is_ok = False
    elif code >= 400:
        is_ok = False

    if not is_ok:
        raise ApiException(code, json_response.get("errors") or json_response.get("message") or body, request_info)

    return json_response


def prepare_dict(
        dict_: typing.Optional[typing.Dict[str, typing.Any]]
) -> typing.Dict[str, typing.Any]:
    """
    Prepare dict for request
    :param dict_: dict for prepare
    :return: prepared dict
    """

    if dict_ is None:
        dict_ = {}
    else:
        dict_ = {name: value for name, value in dict_.items() if value is not None}

    return dict_
