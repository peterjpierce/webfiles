from datetime import datetime as dtime, timedelta as tdelta
import os.path
import re

from flask import request, session, send_file

from webfiles.util.filesystem import Directory
from webfiles.errors import InvalidRequestError, InvalidSessionError
import webfiles.util.auth as auth

import settings.config as config
import settings.users as users


def authenticate():
    """Checks current request and sets session values if good."""
    if auth.is_valid_login(request.form['username'], request.form['password']):
        session['username'] = request.form['username']
        session['last_check'] = dtime.now()
        return True
    else:
        return False


def logout():
    """Log the user out by disabling the session."""
    try:
        for attr in ['username', 'last_check']:
            del session[attr]
    except KeyError as err:
        pass


def check_session():
    """Raise InvalidSessionError if user not logged in or idle too long."""
    too_old = dtime.now() - tdelta(minutes=config.TIMEOUT_MINUTES)
    print('   too_old: %s' % too_old.strftime('%Y-%m-%d %H:%M:%S'))
    print('last_check: %s' % session['last_check'].strftime('%Y-%m-%d %H:%M:%S'))
    try:
        if session['username'] in users.ALLOWED:
            if session['last_check'] > too_old:
                session['last_check'] = dtime.now()
                return True
    except KeyError as err:
        pass
    # bad session if we fell through
    logout()
    raise InvalidSessionError('not logged in')


def _catalog_root():
    """Derive the root directory for this session's files."""
    try:
        rootdir = os.path.join(
                config.FILES_ROOT, auth.get_user_catalog(session['username']))
    except KeyError as err:
        rootdir = None
    return rootdir


def listdir(subdir=''):
    """List files in config.FILE_ROOT or an optional subdirectory."""
    check_session()
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
    check_session()
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
