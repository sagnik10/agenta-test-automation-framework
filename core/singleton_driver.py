class SingletonDriver:
    """Thread-safe Singleton manager for driver instances.

    Ensures that each pytest-xdist worker receives exactly **one**
    driver instance, preventing accidental reuse across tests.

    Attributes:
        _instances (dict): Maps worker IDs and platform keys to driver objects.

    Methods:
        get_instance(platform_key, create_fn):
            Returns existing driver instance if present; otherwise creates one.
        reset():
            Clears all stored singleton instances (typically at teardown).
    """
    _instances = {}

    @classmethod
    def get_instance(cls, key, creator):
        if key not in cls._instances:
            cls._instances[key] = creator()
        return cls._instances[key]

    @classmethod
    def reset(cls):
        cls._instances.clear()
