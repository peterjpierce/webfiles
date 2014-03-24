import os.path
import re

import flask

from webfiles.filesystem import Directory
from webfiles.errors import InvalidRequestError

import settings.config as config


def listdir(subdir=''):
    """List files in config.FILE_ROOT or an optional subdirectory."""
    dr = Directory(config.FILES_ROOT)
    entries = [e for e in dr.listing(subdir) if e.pathtype == 'file']
    return entries


def stream_file(path_tail):
    """Stream the given file if authenticated and permitted.

    Arg path_tail is the path to the file relative to config.FILE_ROOT.
    Raise errors.InvalidRequestError if errors or malicious attempts are
    discovered.
    """
    full = os.path.join(config.FILES_ROOT, path_tail)
    base = os.path.basename(full)

    # validate before sending
    if not os.path.exists(full):
        raise InvalidRequestError('file not found')
    elif not os.path.isfile(full):
        raise InvalidRequestError('request not a file')
    elif re.search('\.\.', path_tail):
        raise InvalidRequestError('request not allowed')
    else:
        return flask.send_file(full, attachment_filename=base, as_attachment=True)
