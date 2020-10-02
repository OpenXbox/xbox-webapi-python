"""
Special Exception subclasses
"""


class XboxException(Exception):
    """Base exception for all Xbox exceptions to subclass"""

    pass


class AuthenticationException(XboxException):
    """Raised when logging in fails, likely due to incorrect auth credentials"""

    pass


class TwoFactorAuthRequired(XboxException):
    def __init__(self, message, server_data):
        """
        Raised when 2FA is required

        Args:
            message (str): Exception message
            server_data (dict): Server data dict, extracted js object from windows live auth request
        """
        super().__init__(message)
        self.server_data = server_data


class InvalidRequest(XboxException):
    def __init__(self, message, response):
        """
        Raised when something is wrong with the request

        Args:
            message (str): error message returned by the server
            response (requests.Response): Instance of :class:`requests.Response`

        """
        self.message = message
        self.response = response


class NotFoundException(XboxException):
    """Any exception raised due to a resource being missing will subclass this"""

    pass
