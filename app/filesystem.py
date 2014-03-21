import datetime
import operator
import os
import os.path
import re

import app.errors as errors
import app.mappings as mappings
from app.shared import Record


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
                self._load_extras()
            elif os.path.isdir(arg):
                self.pathtype = 'directory'
            else:
                self.pathtype = None
        except OSError as err:
            raise errors.PathError(err)
        except Exception as err:
            raise

    def _load_extras(self):
        """Infer display name and date of data for this file, if mapped."""
        self.data_date = None
        self.display_name = self.basename

        for pattern in mappings.PATTERNS:
            hit = re.search(pattern['regex'], self.basename)

            if hit:
                self.display_name = pattern['display_name']

                try:
                    self.revision = hit.group(pattern['revision_group'])
                except (KeyError, IndexError, ValueError) as err:
                    pass

                try:
                    self.data_date = datetime.datetime.strptime(
                            hit.group(pattern['date_regex_group']),
                            pattern['strptime_pattern']
                            )
                except (KeyError, IndexError, ValueError) as err:
                    pass


                break

    def __repr__(self):
        return '<%s: %s>' % (self.__class__, self.basename)


class Directory():
    """Operations on a directory and its contents."""

    def __init__(self, base_directory):
        """Set root point when instantiating.

        Raises PathError if trouble encountered.
        """
        if os.path.isdir(base_directory):
            self.basedir = os.path.abspath(base_directory)
        else:
            raise errors.PathError('invalid directory: %s' % base_directory)

    def listing(self, subdir='', sortby='basename', reverse=True):
        """Provide list of FileRecord for directory contents.

        Arg sortby may be any attribute of FileRecord, but normally one
        of ('basename', 'display_name', 'size', 'data_date').
        """
        dr = os.path.join(self.basedir, subdir)
        field_of = operator.attrgetter(sortby)

        try:
            rawlist = [FileRecord(dr, e) for e in os.listdir(dr)]
            return sorted(rawlist, key = lambda x: field_of(x), reverse=reverse)
        except Exception as err:
            raise

    def __repr__(self):
        return '<%s: %s>' % (self.__class__, self.basedir)
