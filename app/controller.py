import re

import flask

from app.filesystem import Directory, FileRecord
from app.errors import InvalidRequestError

import config


def listdir(directory, subdir=''):
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
    # check for valid arg and file that exists (via FileRecord)
    try:
        filerec = FileRecord(config.FILES_ROOT, path_tail)
    except Exception as err:
        raise InvalidRequestError('file not found')

    # disallow traversing up the filesystem
    if re.search('\.\.', path_tail):
        raise InvalidRequestError('request not allowed')
    # allow only files
    elif not filerec.pathtype == 'file':
        raise InvalidRequestError('request not a file')
    else:
        return flask.send_file(
                filerec.fullpath,
                attachment_filename=filerec.basename,
                as_attachment=True,
                )
