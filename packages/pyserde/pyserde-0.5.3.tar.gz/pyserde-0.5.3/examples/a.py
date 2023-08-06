from dataclasses import dataclass
from typing import Optional

from serde import deserialize, from_dict


def deserialize_maybe_str(_typ, value):
    return value


@deserialize
# @deserialize(deserializer=deserialize_maybe_str)
@dataclass
class CustomDe:
    maybe_str: Optional[str]


if __name__ == "__main__":
    data = {"maybe_str": "bye"}
    print(f"from_dict({data}) = {from_dict(CustomDe, data)}")
