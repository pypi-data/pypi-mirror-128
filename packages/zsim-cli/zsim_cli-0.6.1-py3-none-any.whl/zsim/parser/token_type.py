from typing import NamedTuple

class TokenType(NamedTuple):
    type: str
    regex: str
    skip: bool
