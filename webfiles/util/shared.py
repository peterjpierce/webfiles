class Record:
    """Base class upon which specific types are derived."""

    def __init__(self):
        pass

    def get_field(self, name):
        """Get the value of a named attribute."""
        return self.__dict__[name]

    def set_field(self, name, value):
        """Set named attribute to the given value."""
        self.__dict__[name] = value
        return None

    def loaddict(self, datadict):
        """Loads dictionary into attributes named to match its keys."""
        for k,v in datadict.items():
            self.set_field(k, v)

    @property
    def data(self):
        """Return copy, not direct access."""
        return dict(self.__dict__)
