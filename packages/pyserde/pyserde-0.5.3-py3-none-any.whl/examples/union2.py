from dataclasses import dataclass
from typing import Union, Optional
from serde import toml, deserialize


@deserialize
@dataclass
class TestClass:
    a: Union[None, int, float, Union[tuple[int,float], tuple[float,int], tuple[int,int], tuple[float,float]]]


if __name__ == '__main__':
    test_class = toml.from_toml(TestClass, 'a = 4.1')
    print(test_class)

    # a: Union[None, int, float, tuple[Union[int,float], Union[int,float]]]
    # a: Optional[tuple[Union[int,float], Union[int,float]]]
