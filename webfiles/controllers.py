import logging
import os.path
import re

from flask import request, session, send_file

import settings.config as config
from webfiles.errors import InvalidRequestError
from webfiles.util.decorators import validate_session
from webfiles.util.filesystem import Directory
import webfiles.util.auth as auth

log = logging.getLogger(__name__)


def authenticate():
    """Attempt to log in."""
    results = auth.login(request.form['username'], request.form['password'])
    if results:
        log.info('%s logged in from %s' % (
            session['username'], request.remote_addr))
    else:
        log.info('error logging in from %s' % request.remote_addr)
    return results


def logout():
    """Log the user out."""
    log.info('%s is logging out' % session['username'])
    return auth.logout()


def _catalog_root(catalog):
    """Derive the root directory for this session's files."""
    return os.path.join(config.FILES_ROOT, catalog)


@validate_session
def listdir(subdir=''):
    """List files in config.FILE_ROOT or an optional subdirectory."""
    catalog = auth.get_user_catalog(session['username'])
    croot = _catalog_root(catalog)
    log.debug('%s (%s) is listing /%s' % (session['username'], catalog, subdir))
    dr = Directory(croot)
    entries = [e for e in dr.listing(subdir) if e.pathtype == 'file']
    return entries


@validate_session
def stream_file(path_tail):
    """Stream the given file if authenticated and permitted.

    Arg path_tail is the path to the file relative to config.FILE_ROOT.
    Raise errors.InvalidRequestError if errors or malicious attempts are
    discovered.
    """
    catalog = auth.get_user_catalog(session['username'])
    croot = _catalog_root(catalog)
    log.info('%s (%s) is downloading %s' % (session['username'], catalog, path_tail))
    full = os.path.join(croot, path_tail)
    base = os.path.basename(full)

    # validate before sending
    error_msg = None
    if not os.path.exists(full):
        error_msg = 'file not found'
    elif not os.path.isfile(full):
        error_msg = 'request not a file'
    elif re.search('\.\.', path_tail):
        error_msg = 'request not allowed'

    if error_msg:
        log.warn('%s encountered error "%s"' % (session['username'], error_msg))
        raise InvalidRequestError(error_msg)
    else:
        return send_file(full, attachment_filename=base, as_attachment=True)
