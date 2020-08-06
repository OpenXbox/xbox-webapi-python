"""
Message - Read and send messages
"""
from pathlib import Path
from xbox.webapi.api.provider.baseprovider import BaseProvider


class MessageProvider(BaseProvider):
    MSG_URL = "https://xblmessaging.xboxlive.com"
    HEADERS_MESSAGE = {'x-xbl-contract-version': '1'}


    def get_message_inbox(self):
        """
        Get message inbox

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.MSG_URL + "/network/xbox/users/xuid(%s)/inbox" % self.client.xuid
        return self.client.session.get(url, params=params, headers=self.HEADERS_MESSAGE)


    def get_conversation(self, xuid):
        """
        Get detailed message info

        Args:
            xuid (str): XUID of chat participant

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if not isinstance(xuid, str):
            raise TypeError('Expecting XUID string')

        url = self.MSG_URL + "/network/xbox/users/xuid(%s)/conversations/users/xuid(%s)?maxItems=100" % (self.client.xuid, xuid)
        return self.client.session.get(url, headers=self.HEADERS_MESSAGE)


    def send_message(self, message_text, xuid):
        """
        Send message to a XUID

        Args:
            message_text: text message
            xuid: id of recipient

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if not isinstance(xuid, str):
            raise TypeError('Expecting XUID string')

        if not isinstance(message_text, str):
            raise TypeError('Expecting message_text string')
        elif len(message_text) > 256:
            raise ValueError('Message text exceeds max length of 256 chars')

        url = self.MSG_URL + "/network/xbox/users/xuid(%s)/conversations/users/xuid(%s)" % (self.client.xuid, xuid)
        post_data = {
            'parts': [
             {
                'text': message_text,
                'contentType':'text',
                'version':0
             }]
	}
        return self.client.session.post(url, json=post_data, headers=self.HEADERS_MESSAGE)


    def send_image(self, image_url, xuid, media_type="unknown", message_text="unknown"):
        """
        Send an image to a XUID

        Args:
            message_text: optional message text
            image_url: url to image file
            media_type: extension/filetype of provided image
            xuid: id of recipient

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if not isinstance(xuid, str):
            raise TypeError('Expecting XUID string')

        if not isinstance(message_text, str):
            raise TypeError('Expecting message_text string')
        elif len(message_text) > 256:
            raise ValueError('Message text exceeds max length of 256 chars')
        elif message_text == "unknown":
             message_text = image_url

        if not isinstance(image_url, str):
            raise TypeError('Expecting image_url string')
        elif len(image_url) > 256:
            raise ValueError('Image URL exceeds max length of 256 chars')

        if not isinstance(media_type, str):
            raise TypeError('Expecting image_url string')
        elif len(media_type) > 256:
            raise ValueError('Image URL exceeds max length of 256 chars')
        elif media_type == "unknown":
             media_type = Path(image_url).suffix


        url = self.MSG_URL + "/network/xbox/users/xuid(%s)/conversations/users/xuid(%s)" % (self.client.xuid, xuid)
        post_data = {
            'parts': [
             {
                'text': message_text,
                'mediaUri': image_url,
                'shouldObscure':False,
                'contentType':'weblinkMedia',
                'mediaType':media_type,
                'version':0
             }]
	}
        return self.client.session.post(url, json=post_data, headers=self.HEADERS_MESSAGE)
