# Standard library
import re
from functools import reduce
from typing import Dict

# Internal modules
from resttest.models import Env


def resolve_dict(env: Env, body: Dict) -> Dict:
    final_body: Dict = {}
    for key, val in body.items():
        if isinstance(val, str):
            final_body[key] = resolve_value(env, val)
        elif isinstance(val, dict):
            final_body[key] = resolve_dict(env, val)
        else:
            final_body[key] = val
    return final_body


def resolve_value(env: Env, val: str) -> str:
    matches = re.findall(r"\${(.*?)\}", val)
    return reduce(
        lambda templ, match: templ.replace("${" + match + "}", env.data[match]),
        matches,
        val,
    )

