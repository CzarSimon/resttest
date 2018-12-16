# Standard library
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Env:
    base_url: str
    data: Dict[str, str]


@dataclass(frozen=True)
class Request:
    method: str
    path: str
    body: Optional[Dict[str, Any]]
    useToken: bool


@dataclass(frozen=True)
class Response:
    status: int
    body: Optional[Dict[str, Any]]


@dataclass(frozen=True)
class EnvUpdate:
    env_key: str
    response_key: str


@dataclass(frozen=True)
class TestCase:
    name: str
    request: Request
    response: Response
    set_env: Optional[List[EnvUpdate]]
