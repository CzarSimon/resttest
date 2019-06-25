# Standard library
import re
from functools import reduce
from typing import Dict

# Internal modules
from resttest.models import TestCase, Request, Response, Env
from .template_util import resolve_dict, resolve_value

# 3rd party modules
import requests


def make_request(req: Request, env: Env) -> Response:
    if req.method in ("GET", "DELETE"):
        return _make_request_without_body(req, env)
    return _make_request_with_body(req, env)


def _make_path(req: Request, env: Env) -> str:
    path = env.base_url + req.path
    for key, val in env.data.items():
        path_key = "${" + key + "}"
        path = path.replace(path_key, val)
    return path


def _make_request_without_body(req: Request, env: Env) -> Response:
    url = _make_path(req, env)
    headers = _make_headers(env, req)
    resp = requests.request(req.method, url, headers=headers)
    return _map_response(resp)


def _make_request_with_body(req: Request, env: Env) -> Response:
    if not req.body:
        return _make_request_without_body(req, env)
    url = _make_path(req, env)
    headers = _make_headers(env, req)
    body = resolve_dict(env, req.body)
    resp = requests.request(req.method, url, json=body, headers=headers)
    return _map_response(resp)


def _make_headers(env: Env, req: Request) -> Dict[str, str]:
    headers = {"Content-Type": "application/json", "X-Client-ID": env.data["clientId"]}
    for key, val in req.headers.items():
        headers[key] = resolve_value(env, val)
    return headers


def _map_response(resp: requests.Response) -> Response:
    return Response(status=resp.status_code, body=resp.json())

