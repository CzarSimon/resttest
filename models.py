# Standard library
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Env:
    base_url: str
    data: Dict[str, str]

    @classmethod
    def fromdict(cls, port: int, raw: Dict[str, Any]) -> "cls":
        base_url = raw["baseUrl"] if "baseUrl" in raw else f"http://127.0.0.1:{port}"
        return cls(base_url=base_url, data=raw["data"])


@dataclass(frozen=True)
class Request:
    method: str
    path: str
    body: Optional[Dict[str, Any]]
    use_token: bool

    @classmethod
    def fromdict(cls, raw: Dict[str, Any]) -> "cls":
        return cls(
            method=raw["method"],
            path=raw["raw"],
            body=raw["body"] if "body" in raw else None,
            use_token=raw["useToken"],
        )


@dataclass(frozen=True)
class Response:
    status: int
    body: Optional[Dict[str, Any]]

    @classmethod
    def fromdict(cls, raw: Dict[str, Any]) -> "cls":
        return cls(method=raw["status"], body=raw["body"] if "body" in raw else None)


@dataclass(frozen=True)
class EnvUpdate:
    env_key: str
    response_key: str

    @classmethod
    def fromdict(cls, raw: Dict[str, Any]) -> "cls":
        return cls(env_key=raw["env_key"], response_key=raw["response_key"])


@dataclass(frozen=True)
class TestCase:
    name: str
    request: Request
    response: Response
    set_env: List[EnvUpdate]

    @classmethod
    def fromdict(cls, raw: Dict[str, Any]) -> "cls":
        updates: List[EnvUpdate] = []
        if "setEnv" in raw:
            updates = [EnvUpdate.fromdict(u) for u in raw["setEnv"]]

        return cls(
            name=raw["name"],
            request=Request.fromdict(raw["request"]),
            response=Response.fromdict(raw["response"]),
            set_env=updates,
        )
