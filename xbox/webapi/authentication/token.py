"""
Token containers
"""
from datetime import datetime, timedelta


class Token(object):
    def __init__(self, jwt, date_issued, date_valid):
        """
        Container for authentication tokens obtained from Windows Live / Xbox Live Servers, featuring validity checking.

        Args:
            token (str): The JWT Token
            date_issued (str/datetime): The date the token was issued. Just provide the current time if you do not
            have this info.
            date_valid (str/datetime): The date the token expires.

        Returns:
            Token: Instance of :class:`Token`
        """
        self.jwt = jwt

        if isinstance(date_issued, str):
            date_issued = _parse_ts(date_issued)
        self.date_issued = date_issued

        if isinstance(date_valid, str):
            date_valid = _parse_ts(date_valid)
        self.date_valid = date_valid

    @classmethod
    def from_dict(cls, node):
        """
        Assemble a :class:`Token` object from a dict, for example from json config file.

        Args:
            node (dict): Token as `dict` object. Mandatory fields: 'token', 'date_issued', 'date_valid'

        Returns:
            Token: Instance of :class:`Token`

        """
        name = node['name']

        token_classes = {
            'AccessToken': AccessToken,
            'RefreshToken': RefreshToken,
            'UserToken': UserToken,
            'DeviceToken': DeviceToken,
            'TitleToken': TitleToken,
            'XSTSToken': XSTSToken
        }

        if name not in token_classes:
            raise ValueError('Invalid token name %s' % name)

        token_cls = token_classes[name]
        instance = token_cls.__new__(token_cls)
        super(token_cls, instance).__init__(
            node['jwt'], node['date_issued'], node['date_valid']
        )
        return instance

    def to_dict(self):
        """
        Convert the `Token`-object to a `dict`-object, to use it in json-file for example.
        Returns:
            dict: The token formatted as dict.
        """
        return {
            'name': self.__class__.__name__,
            'jwt': self.jwt,
            'date_issued': self.date_issued.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'date_valid': self.date_valid.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }

    @property
    def is_valid(self):
        """
        Check if token is still valid.

        Returns:
            bool: True on success, False otherwise

        """
        return self.date_valid > datetime.utcnow()

    def __str__(self):
        return "<%s, is_valid=%s, jwt=%s, issued=%s, expires=%s>" % (
            self.__class__.__name__, self.is_valid, self.jwt, self.date_issued, self.date_valid
        )


class AccessToken(Token):
    def __init__(self, jwt, expires_sec):
        """
        Container for storing Windows Live Access Token

        Subclass of :class:`Token`

        WARNING: Only invoke when creating a FRESH token
        Don't use to convert saved token into object
        Args:
            token (str): The JWT Access-Token
            expires_sec (int): The expiry-time in seconds
        """
        date_issued = datetime.utcnow()
        date_valid = date_issued + timedelta(seconds=int(expires_sec))
        super(AccessToken, self).__init__(jwt, date_issued, date_valid)


class RefreshToken(Token):
    def __init__(self, jwt):
        """
        Container for storing Windows Live Refresh Token.

        Subclass of :class:`Token`

        WARNING: Only invoke when creating a FRESH token!
        Don't use to convert saved token into object
        Refresh Token usually has a lifetime of 14 days

        Args:
            token (str): The JWT Refresh-Token
        """
        date_issued = datetime.utcnow()
        date_valid = date_issued + timedelta(days=14)
        super(RefreshToken, self).__init__(jwt, date_issued, date_valid)


class UserToken(Token):
    """
    Container for storing Xbox Live User Token.

    Subclass of :class:`Token`

    WARNING: Only invoke when creating a FRESH token!
    Don't use to convert saved token into object
    """
    pass


class DeviceToken(Token):
    """
    Container for storing Xbox Live Device Token.

    Subclass of :class:`Token`

    WARNING: Only invoke when creating a FRESH token!
    Don't use to convert saved token into object
    """
    pass


class TitleToken(Token):
    """
    Container for storing Xbox Live Title Token.

    Subclass of :class:`Token`

    WARNING: Only invoke when creating a FRESH token!
    Don't use to convert saved token into object
    """
    pass


class XSTSToken(Token):
    """
    Container for storing Xbox Live XSTS Token.

    Subclass of :class:`Token`

    WARNING: Only invoke when creating a FRESH token!
    Don't use to convert saved token into object
    """
    pass


def _parse_ts(s):
    if '.' in s:
        idx = s.index('.') - 2
        parts = s[:idx], s[idx:-1]
        if len(parts[1]) > 6:
            micro = float(parts[1])
            s = '{:s}{:f}Z'.format(parts[0], micro)

    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
