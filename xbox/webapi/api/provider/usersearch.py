"""
Usersearch - Search for gamertags / userprofiles
"""


class UserSearchProvider(object):
    USERSEARCH_URL = "https://usersearch.xboxlive.com"
    HEADERS_USER_SEARCH = {'x-xbl-contract-version': '1'}

    def __init__(self, client):
        """
        Initialize an instance of UserSearchProvider

        Args:
            client (:class:`XboxLiveClient`): Instance of XboxLiveClient
        """
        self.client = client

    def get_live_search(self, query):
        """
        Get userprofiles for search query

        Args:
            query (str): Search query

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.USERSEARCH_URL + "/suggest?"
        params = {
            "q": query
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_USER_SEARCH)
