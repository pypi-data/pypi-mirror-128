"""Define the singleton metaclass."""


class Singleton(type):
    """Implementation of the singleton pattern as a meta class."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Override call method of inheriting class."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
