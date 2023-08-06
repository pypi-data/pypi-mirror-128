import datetime
from dataclasses import dataclass

from serde import deserialize, serialize
from serde.json import from_json, to_json


@deserialize
@serialize
@dataclass
class Foo:
    d: datetime.date
    t: datetime.time
    dt: datetime.datetime


def main():
    dt = datetime.datetime(2021, 1, 1, 0, 0, 0)

    foo = Foo(dt.date(), dt.time(), dt)
    print(f"Into Json: {to_json(foo)}")

    s = '{"d": "2021-01-01", "t": "00:00:00", "dt": "2021-01-01T00:00:00"}'
    print(f"From Json: {from_json(Foo, s)}")


if __name__ == '__main__':
    main()
