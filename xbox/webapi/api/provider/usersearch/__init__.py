"""
Usersearch - Search for gamertags / userprofiles
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.usersearch.models import UserSearchResponse


class UserSearchProvider(BaseProvider):
    USERSEARCH_URL = "https://usersearch.xboxlive.com"
    HEADERS_USER_SEARCH = {"x-xbl-contract-version": "1"}

    async def get_live_search(self, query: str) -> UserSearchResponse:
        """
        Get userprofiles for search query

        Args:
            query: Search query

        Returns:
            :class:`UserSearchResponse`: User Search Response
        """
        url = self.USERSEARCH_URL + "/suggest"
        params = {"q": query}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_USER_SEARCH
        )
        resp.raise_for_status()
        return UserSearchResponse.parse_raw(await resp.text())
