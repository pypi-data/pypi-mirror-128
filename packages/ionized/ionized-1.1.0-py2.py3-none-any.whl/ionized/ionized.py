"""Main module.

Usage:

    ...
    from dataclasses import dataclass
    from ionized import ionize

    @dataclass
    @ionize
    class MyDataclass:
        name: str
        age: int


    my_instance = MyDataclass(name='Patrick', age=24)
    encoded = my_instance.ionize()

    my_instance = MyDataclass.deionize(encoded)
"""
import amazon.ion.simpleion as ion


def ionize(cls):
    """Wrapper to implement the `ionize` method."""
    class Wrapper:
        """Wrapped `cls` instance."""

        def __init__(self, *args, **kwargs):
            self.wrap = cls(*args, **kwargs)

        def ionize(self):
            """Dump the dataclass content to a Amazon Ion format."""
            # fetches the name attribute
            data = {
                k: getattr(self.wrap, k)
                for k in self.wrap.__annotations__.keys()
            }

            return ion.dumps(data)

        @classmethod
        def deionize(cls, payload):
            """Create an instance from an Ion Payload."""
            data = ion.loads(payload, single_value=True)
            if not isinstance(data, ion.IonPyDict):
                raise ValueError(
                    f"Data must be castablein {ion.IonPyDict}"
                )
            _data_as_dict = dict(data.items())
            return cls(_data_as_dict)

    return Wrapper


__all__ = [
    'ionize',
]
