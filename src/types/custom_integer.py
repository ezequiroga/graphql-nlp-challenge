
from typing import NewType
import strawberry


Integer = strawberry.scalar(
    NewType("Integer", int),
    serialize=lambda v: int(v) if v is not None and not v == '' else 0,
    parse_value=lambda v: str(v),
)
