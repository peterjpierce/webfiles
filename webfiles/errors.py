class BaseError(Exception):
    """Base class from which all others are derived."""
    pass


class PathError(BaseError):
    """Raised when a directory or file does not exist."""
    pass


class InvalidRequestError(BaseError):
    """Raised when a malicious request or erroneous file path received."""
    pass


class InvalidSessionError(BaseError):
    """Raised when a request is attempted but the session is not authenticated."""
    pass
