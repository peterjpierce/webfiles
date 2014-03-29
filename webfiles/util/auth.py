from datetime import datetime as dtime, timedelta as tdelta
import hashlib

from flask import session

import settings.users as users
import settings.config as config

ENCODING = 'utf-8'


def get_user_catalog(username):
    """Check for and provide a user's catalog name."""
    try:
        return users.ALLOWED[username]['catalog']
    except KeyError as err:
        return None


def is_valid_login(username, password):
    """Check credentials and return their catalog name."""
    hashword = hashlib.md5(password.encode(ENCODING)).hexdigest()
    return (username in users.ALLOWED and users.ALLOWED[username]['hashword'] == hashword)


def is_valid_session():
    """Validate a session."""
    stale_threshold = dtime.now() - tdelta(minutes=config.TIMEOUT_MINUTES)
    try:
        too_old = (session['last_check'] < stale_threshold)
        if session['username'] in users.ALLOWED and not too_old:
            return True
    except KeyError as err:
        pass
    # bad session if we fell through
    return False


def login(username, password):
    """Checks current request and sets session values if good."""
    if is_valid_login(username, password):
        session['username'] = username
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
