"""
BaseProvider

Subclassed by every *real* provider
"""


class BaseProvider:
    def __init__(self, client):
        """
        Initialize an the BaseProvider

        Args:
            client (:class:`XboxLiveClient`): Instance of XboxLiveClient
        """
        self.client = client
