"""
Example script that utilizes EDSProvider to search XBL marketplace
"""
import argparse
import asyncio
from pprint import pprint
import sys

from httpx import HTTPStatusError, AsyncClient

from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager


async def async_main():
    parser = argparse.ArgumentParser(description="Search for Content on XBL")
    parser.add_argument("search_query", help="Name to search for")

    args = parser.parse_args()

    async with AsyncClient() as session:
        auth_mgr = AuthenticationManager(session, "", "", "")

        # No Auth necessary for catalog searches
        xbl_client = XboxLiveClient(auth_mgr)

        try:
            resp = await xbl_client.catalog.product_search(args.search_query)
        except HTTPStatusError:
            print("Search failed")
            sys.exit(-1)

        pprint(resp.dict())


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
