"""
Container for userinfo, received by Xbox Live Authorization
"""


class XboxLiveUserInfo(object):
    def __init__(self, xuid, userhash, gamertag, age_group, privileges, user_privileges):
        """
        Initialize a new instance of :class:`XboxLiveUserInfo`

        Args:
            xuid (str): Xbox User ID
            userhash (str): Xbox Live Userhash
            gamertag (str): Xbox Gamertag
            age_group (str): Xbox Live age-group
            privileges (str): Privileges
            user_privileges (str): User privileges
        """
        self.xuid = xuid
        self.userhash = userhash
        self.gamertag = gamertag
        self.age_group = age_group
        self.privileges = privileges
        self.user_privileges = user_privileges

    @classmethod
    def from_dict(cls, node):
        """
        Initialize a new instance via json data

        Args:
            node (dict): A dict holding userinfo fields

        Returns:
            Instance of :class:`XboxLiveUserInfo`
        """
        return cls(node['xid'], node['uhs'], node['gtg'], node['agg'], node.get('prv'), node.get('usr'))

    def to_dict(self):
        """
        Get class members as dict

        Returns:
            dict: Xbox Live userinfo
        """
        return {
            'xid': self.xuid,
            'uhs': self.userhash,
            'gtg': self.gamertag,
            'agg': self.age_group,
            'prv': self.privileges,
            'usr': self.user_privileges
        }

    def __str__(self):
        return '<%s, gamertag=%s, uhs=%s, xuid=%s>' % (
            self.__class__.__name__, self.gamertag, self.userhash, self.xuid
        )
