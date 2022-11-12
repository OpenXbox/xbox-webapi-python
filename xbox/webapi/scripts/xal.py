"""
Example scripts that performs XBL authentication via XAL
"""
import argparse
import asyncio
import json
import os
import uuid

from pydantic import BaseModel
from pydantic.json import pydantic_encoder

from xbox.webapi.authentication.models import (
    SisuAuthorizationResponse,
    XalAppParameters,
    XalClientParameters,
)
from xbox.webapi.authentication.xal import (
    APP_PARAMS_GAMEPASS_BETA,
    CLIENT_PARAMS_ANDROID,
    XALManager,
)
from xbox.webapi.common.signed_session import SignedSession
from xbox.webapi.scripts import XAL_TOKENS_FILE


class XALStore(BaseModel):
    """Used to store/load authorization data"""

    sisu: SisuAuthorizationResponse
    device_id: uuid.UUID
    app_params: XalAppParameters
    client_params: XalClientParameters


def user_prompt_authentication(auth_url: str) -> str:
    """
    Handles the auth callback when user is prompted to authenticate via URL
    in webbrowser

    Takes the redirect URL from stdin
    """

    redirect_url = input(
        f"Continue auth with the following URL:\n\n"
        f"URL: {auth_url}\n\n"
        f"Provide redirect URI: "
    )
    return redirect_url


async def do_auth(device_id: uuid.UUID, token_filepath: str):
    async with SignedSession() as session:
        app_params = APP_PARAMS_GAMEPASS_BETA
        client_params = CLIENT_PARAMS_ANDROID

        store = None
        # Load existing sisu authorization data, if it exists
        if os.path.exists(token_filepath):
            with open(token_filepath) as f:
                store = json.load(f)

            # Convert SISU authorization data
            store = XALStore(**store)

        if store:
            raise NotImplementedError("Token refreshing")

        # Do authentication
        xal = XALManager(session, device_id, app_params, client_params)
        response = await xal.auth_flow(user_prompt_authentication)
        print(f"Sisu auth finished:\n\n{response}")

        # Save authorization data
        store = XALStore(
            sisu=response,
            device_id=device_id,
            app_params=app_params,
            client_params=client_params,
        )

        with open(token_filepath, mode="w") as f:
            print(f"Finished authentication, writing tokens to {token_filepath}")
            json.dump(store, f, default=pydantic_encoder)


async def async_main():
    parser = argparse.ArgumentParser(description="Authenticate with XBL via XAL")
    parser.add_argument(
        "--tokens",
        "-t",
        default=XAL_TOKENS_FILE,
        help=f"Token filepath. Default: '{XAL_TOKENS_FILE}'",
    )
    parser.add_argument(
        "--device-id",
        "-did",
        default=uuid.uuid4(),
        type=uuid.UUID,
        help="Device ID (for device auth)",
    )
    args = parser.parse_args()

    await do_auth(args.device_id, args.tokens)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
