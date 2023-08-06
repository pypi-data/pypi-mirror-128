#!/usr/bin/env python
"""Tests for `ionized` package."""
from dataclasses import dataclass
from ionized.ionized import ionize


def test_simple_dataclass():

    @ionize
    @dataclass
    class MyData:
        name: str

    simple_class = MyData("John")
    print(simple_class.ionize())


def test_multiple_attr():
    """Ensure we can se multiple simple attributes."""
    @ionize
    @dataclass
    class MyDataclass:
        name: str
        age: int = 0

    my_instance = MyDataclass('Patrick', 12)
    encoded = my_instance.ionize()
    assert encoded == b'\xe0\x01\x00\xea\xea\x81\x83\xde\x86\x87\xb4\x83age\xde\x8c\x84\x87Patrick\x8a!\x0c'
