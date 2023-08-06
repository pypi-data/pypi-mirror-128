from dataclasses import dataclass
from typing import Optional, Union, Tuple
import typing
import pathlib

from serde import deserialize, from_dict


def deserialize_maybe_str(_typ, value):
    return value


@deserialize(deserializer=deserialize_maybe_str)
@dataclass
class CustomDe:
    maybe_str: Tuple[pathlib.Path, int]


if __name__ == "__main__":
    data = {"maybe_str": ["bye", 10]}
    print(f"from_dict({data}) = {from_dict(CustomDe, data)}")
