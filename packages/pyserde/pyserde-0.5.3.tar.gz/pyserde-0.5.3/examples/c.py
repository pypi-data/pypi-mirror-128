from dataclasses import dataclass

from serde import deserialize, serialize
from serde.toml import from_toml

@deserialize
@serialize
@dataclass
class Test:
    foo: float

test = from_toml(Test, """
        foo = "test"
        """
        )
print(test)
