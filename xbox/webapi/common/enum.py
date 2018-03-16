"""
Enum helper class
"""


class EnumType(type):
    """
    Metaclass for enums. Creates a reverse lookup dictionary upon class initialization.
    """
    def __init__(cls, name, bases, d):
        type.__init__(cls, name, bases, d)
        cls.__reverse = dict((value, key) for key, value in d.items())

    def __contains__(cls, item):
        return item in cls.__dict__ or item in cls.__reverse

    def __getitem__(cls, item):
        if item in cls.__reverse:
            return cls.__reverse[item]
        raise AttributeError(item)


class Enum(metaclass=EnumType):
    """
    Helper class that sets `EnumType` as its metaclass so that enums can just subclass `Enum`.
    """
    __metaclass__ = EnumType
