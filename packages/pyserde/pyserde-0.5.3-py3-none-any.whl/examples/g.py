from dataclasses import dataclass

@dataclass
class Foo:
    a: int
    def __init__(self, a):
        self.a = a
        print(globals())


if __name__ == '__main__':
    print(globals())
    Foo(10)
