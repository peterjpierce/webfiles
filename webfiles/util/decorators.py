from datetime import datetime as dtime
from functools import wraps

from flask import session, url_for, redirect

import webfiles.errors as errors
import webfiles.util.auth as auth


def validate_session(anyfunc):
    """Decorator for controllers to validate and update sessions.

    Raises InvalidSessionError if not authenticated or session too stale.
    """
    @wraps(anyfunc)
    def wrapped(*args, **kwargs):
        if auth.is_valid_session():
            try:
                session['last_check'] = dtime.now()
                return anyfunc(*args, **kwargs)
            except KeyError as err:
                pass
        # bad session if we fell through
        auth.logout()
        raise errors.InvalidSessionError('not logged in')
    return wrapped


def require_logged_in(anyfunc):
    """Decorator for views to enforce authentication.

    Redirects to url_for('login') which must be a valid route for this to work.

    This also traps any InvalidSessionError coming from the controller, which
    were probably raised by @validate_session decorator above, so there is
    no need to try...except explicitly in the view.
    """
    @wraps(anyfunc)
    def wrapped(*args, **kwargs):
        try:
            if auth.is_valid_session():
                return anyfunc(*args, **kwargs)
        except errors.InvalidSessionError as err:
            pass
        # bad session if we fell through
        auth.logout()
        return redirect(url_for('login'))
    return wrapped
