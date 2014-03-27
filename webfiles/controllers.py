import os.path
import re

from flask import session, send_file

from webfiles.util.filesystem import Directory
from webfiles.errors import InvalidRequestError

import settings.config as config


def _catalog_root():
    """Derive the root directory for this session's files."""
    try:
        rootdir = os.path.join(config.FILES_ROOT, session['catalog'])
    except KeyError as err:
        rootdir = None
    return rootdir


def listdir(subdir=''):
    """List files in config.FILE_ROOT or an optional subdirectory."""
    croot = _catalog_root()
    dr = Directory(croot)
    entries = [e for e in dr.listing(subdir) if e.pathtype == 'file']
    return entries


def stream_file(path_tail):
    """Stream the given file if authenticated and permitted.

    Arg path_tail is the path to the file relative to config.FILE_ROOT.
    Raise errors.InvalidRequestError if errors or malicious attempts are
    discovered.
    """
    croot = _catalog_root()
    full = os.path.join(croot, path_tail)
    base = os.path.basename(full)

    # validate before sending
    if not os.path.exists(full):
        raise InvalidRequestError('file not found')
    elif not os.path.isfile(full):
        raise InvalidRequestError('request not a file')
    elif re.search('\.\.', path_tail):
        raise InvalidRequestError('request not allowed')
    else:
        return send_file(full, attachment_filename=base, as_attachment=True)
