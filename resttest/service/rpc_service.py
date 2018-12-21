# Standard library
from typing import Dict

# Internal modules
from resttest.models import TestCase, Request, Response, Env

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
    headers = _make_headers(env, req.use_token)
    resp = requests.request(req.method, url, headers=headers)
    return _map_response(resp)


def _make_request_with_body(req: Request, env: Env) -> Response:
    if not req.body:
        return _make_request_without_body(req, env)
    url = _make_path(req, env)
    headers = _make_headers(env, req.use_token)
    body = _resolve_body(env, req.body)
    resp = requests.request(req.method, url, json=body, headers=headers)
    return _map_response(resp)


def _make_headers(env: Env, with_token: bool) -> Dict[str, str]:
    base_headers = {
        "Content-Type": "application/json",
        "X-Client-ID": env.data["clientId"],
    }
    if with_token:
        base_headers["Authorization"] = f'Bearer {env.data["authToken"]}'
    return base_headers


def _resolve_body(env: Env, body: Dict) -> Dict:
    final_body: Dict = {}
    for key, val in body.items():
        if isinstance(val, str):
            final_body[key] = _resolve_value(env, val)
        elif isinstance(val, dict):
            final_body[key] = _resolve_body(env, val)
        else:
            final_body[key] = val
    return final_body


def _resolve_value(env: Env, val: str) -> str:
    key = val.replace("${", "").replace("}", "")
    if key == val:
        return val
    return env.data[key]


def _map_response(resp: requests.Response) -> Response:
    return Response(status=resp.status_code, body=resp.json())

