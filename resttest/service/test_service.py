# Standard library
import sys
from typing import Any, Dict, List

# Internal modules
from .rpc_service import make_request
from resttest.models import Env, EnvUpdate, TestCase, Response


def run_tests(test_cases: List[TestCase], env: Env) -> None:
    for i, tc in enumerate(test_cases):
        _run_test(i + 1, tc, env)
    print("Great success")


def _run_test(number: int, test_case: TestCase, env: Env) -> None:
    print(f"{number} - {test_case.name}")
    resp = make_request(test_case.request, env)
    _assert_response(test_case, resp)
    if test_case.set_env:
        if not resp.body:
            _fail(test_case, "Env updates specifed but no response body found")
        else:
            _update_env(resp.body, test_case.set_env, env)
    print("OK\n")


def _assert_response(test_case: TestCase, actual: Response) -> None:
    expected_status = test_case.response.status
    if expected_status != actual.status:
        msg = f"Wrong status. Expected: {expected_status} Was: {actual.status}"
        _fail(test_case, msg)
    _assert_body(test_case, actual)


def _assert_body(test_case: TestCase, actual: Response) -> None:
    if not test_case.response.body:
        return
    if actual.body:
        _assert_body_content(test_case, test_case.response.body, actual.body)
    else:
        _fail(test_case, "Missing response body")


def _assert_body_content(
    test_case: TestCase, expected: Dict[str, Any], actual: Dict[str, str]
) -> None:
    for key, expected in expected.items():
        if not key in actual:
            _fail(test_case, f"Missing: {key} in response body.")
        value = actual[key]
        if expected != value:
            _fail(
                test_case,
                f"Unexpected value for {key}. Expected: {expected}. Got: {value}",
            )


def _update_env(
    response_body: Dict[str, str], updates: List[EnvUpdate], env: Env
) -> None:
    for update in updates:
        env_key = update.env_key
        response_key = update.response_key
        env.data[env_key] = response_body[response_key]


def _fail(test_case: TestCase, msg: str) -> None:
    print(f"FAILED: {test_case.name} {msg}\n")
    sys.exit(1)
