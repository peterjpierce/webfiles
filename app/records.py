import datetime
import os.path

import app.errors


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


class FileRecord(Record):
    """Information about a file."""

    def __init__(self, directory_path, filename):
        """Leverage setter property below to also meta info."""
        full = os.path.abspath(os.path.join(directory_path, filename))
        try:
            self.fullpath = full
        except Exception as err:
            raise

    @property
    def fullpath(self):
        return os.path.join(self.dirname, self.basename)

    @fullpath.setter
    def fullpath(self, arg):
        """Set path elements and other metadata like size and type."""
        self.dirname = os.path.dirname(arg)
        self.basename = os.path.basename(arg)
        try:
            self.size = os.path.getsize(arg)
            self.modtime = datetime.datetime.fromtimestamp(
                    os.path.getmtime(arg))
            if os.path.isfile(arg):
                self.pathtype = 'file'
            elif os.path.isdir(arg):
                self.pathtype = 'directory'
            else:
                self.pathtype = None
        except OSError as err:
            raise errors.PathError(err)
        except Exception as err:
            raise

    def __repr__(self):
        return '<%s: %s>' % (self.__class__, self.basename)
