import hashlib

from flask import session

from settings.users import ALLOWED

ENCODING = 'utf-8'


def get_user_catalog(username):
    """Check for and provide a user's catalog name."""
    try:
        return ALLOWED[username]['catalog']
    except KeyError as err:
        return None


def is_valid_login(username, password):
    """Check credentials and return their catalog name."""
    hashword = hashlib.md5(password.encode(ENCODING)).hexdigest()
    return (username in ALLOWED and ALLOWED[username]['hashword'] == hashword)
