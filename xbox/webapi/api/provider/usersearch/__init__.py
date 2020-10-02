"""
Usersearch - Search for gamertags / userprofiles
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider


class UserSearchProvider(BaseProvider):
    USERSEARCH_URL = "https://usersearch.xboxlive.com"
    HEADERS_USER_SEARCH = {"x-xbl-contract-version": "1"}

    async def get_live_search(self, query):
        """
        Get userprofiles for search query

        Args:
            query (str): Search query

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.USERSEARCH_URL + "/suggest?"
        params = {"q": query}
        return await self.client.session.get(
            url, params=params, headers=self.HEADERS_USER_SEARCH
        )
