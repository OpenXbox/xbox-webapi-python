"""
Message - Read and send messages
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider


class MessageProvider(BaseProvider):
    MSG_URL = "https://msg.xboxlive.com"
    HEADERS_MESSAGE = {'x-xbl-contract-version': '1'}

    def get_message_inbox(self, skip_items=0, max_items=100):
        """
        Get messages

        Args:
            skip_items (int): Item count to skip
            max_items (int): Maximum item count to load

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.MSG_URL + "/users/xuid(%s)/inbox" % self.client.xuid
        params = {
            'skipItems': skip_items,
            'maxItems': max_items
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_MESSAGE)

    def get_message(self, message_id):
        """
        Get detailed message info

        Args:
            message_id (str): Message Id

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.MSG_URL + "/users/xuid(%s)/inbox/%s" % (self.client.xuid, message_id)
        return self.client.session.get(url, headers=self.HEADERS_MESSAGE)

    def delete_message(self, message_id):
        """
        Delete message

        **NOTE**: Returns HTTP Status Code **204** on success

        Args:
            message_id (str): Message Id

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.MSG_URL + "/users/xuid(%s)/inbox/%s" % (self.client.xuid, message_id)
        return self.client.session.delete(url, headers=self.HEADERS_MESSAGE)

    def send_message(self, message_text, gamertags=None, xuids=None):
        """
        Send message to a list of gamertags

        Only one of each recipient types can be supplied,
        either gamertags **or** xuids

        Args:
            gamertags (list): List of gamertags

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if not isinstance(message_text, str):
            raise TypeError('Expecting message_text string')
        elif len(message_text) > 256:
            raise ValueError('Message text exceeds max length of 256 chars')

        if gamertags and xuids:
            raise ValueError('Either pass gamertags or xuids, not both!')
        elif gamertags:
            recipients = [dict(gamertag=gtg) for gtg in gamertags]
        elif xuids:
            recipients = [dict(xuid=xid) for xid in xuids]
        else:
            raise ValueError('No recipients are passed')

        url = self.MSG_URL + "/users/xuid(%s)/outbox" % self.client.xuid
        post_data = {
            'header': {
                'recipients': recipients
            },
            'messageText': message_text
        }
        return self.client.session.post(url, json=post_data, headers=self.HEADERS_MESSAGE)
