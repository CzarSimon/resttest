# Standard library
import sys
from typing import Dict, List

# Internal modules
from .rpc_service import make_request
from models import Env, EnvUpdate, TestCase, Response


def run_tests(test_cases: List[TestCase], env: Env) -> None:
    for tc in test_cases:
        run_test(tc, env)


def run_test(test_case: TestCase, env: Env) -> None:
    resp = make_request(test_case.request, env)
    _assert_response(test_case, resp)
    if test_case.set_env:
        _update_env(resp, test_case.set_env, env)


def _assert_response(test_case: TestCase, actual: Response) -> None:
    expected_status = test_case.response.status
    if expected_status != actual.status:
        msg = f"Wrong status. Expected: {expected_status} Was: {actual.status}"
        _fail(test_case, msg)
    _assert_body(test_case, actual)


def _assert_body(test_case: TestCase, actual: Response) -> None:
    if not test_case.response.body:
        return
    if not actual.body:
        _fail(test_case, "Missing response body")
    _assert_body_content(test_case, actual.body)


def _assert_body_content(test_case: TestCase, actual: Dict[str, str]) -> None:
    for key, expected in test_case.response.body:
        if not key in actual:
            _fail(test_case, f"Missing: {key} in response body.")
        value = actual[key]
        if expected != value:
            _fail(
                test_case,
                f"Unexpected value for {key}. Expected: {expected}. Got: {value}",
            )


def _update_env(resp: Response, updates: List[EnvUpdate], env: Env) -> None:
    for update in updates:
        env_key = update.env_key
        response_key = update.response_key
        env.data[env_key] = resp.body[response_key]


def _fail(test_case: TestCase, msg: str) -> None:
    print(f"FAILED: {test_case.name} {msg}\n")
    sys.exit(1)
