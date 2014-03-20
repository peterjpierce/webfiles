import datetime
import os
import os.path
import re

import app.mappings as mappings
import app.errors as errors
from app.records import FileRecord


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

    def listing(self, subdir=''):
        """Provide list of FileRecord for directory contents."""
        dr = os.path.join(self.basedir, subdir)

        try:
            entries = [FileRecord(dr, e) for e in os.listdir(dr)]
        except Exception as err:
            raise

        # load extra fields where possible for files (not dirs)
        for entry in [e for e in entries if e.pathtype == 'file']:
            self._load_extras(entry)

        return entries


    def _load_extras(self, file_record):
        """Infer friendly name and date for this file, if mapped."""
        file_record.mod_date = None
        file_record.friendly_name = file_record.basename

        for pattern in mappings.PATTERNS:
            hit = re.search(pattern['regex'], file_record.basename)

            # load record fields and break out of loop it match found
            if hit:
                file_record.friendly_name = pattern['friendly_name']
                try:
                    dtime = datetime.strptime(
                            hit.group(pattern['date_regex_group']),
                            pattern['strptime_pattern']
                            )
                    file_record.mod_date = dtime.strftime(DATE_DISPLAY)
                except (KeyError, IndexError, ValueError) as err:
                    pass
                else:
                    break
