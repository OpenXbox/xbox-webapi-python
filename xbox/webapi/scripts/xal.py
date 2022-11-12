"""
Example scripts that performs XBL authentication via XAL
"""
import argparse
import asyncio
import json
import os
import sys
import uuid

from pydantic import BaseModel
from pydantic.json import pydantic_encoder

from xbox.webapi.authentication.models import (
    OAuth2TokenResponse,
    SisuAuthorizationResponse,
    XalAppParameters,
    XalClientParameters,
)
from xbox.webapi.authentication.xal import (
    APP_PARAMS_GAMEPASS_BETA,
    CLIENT_PARAMS_ANDROID,
    XALManager,
)
from xbox.webapi.common.request_signer import RequestSigner
from xbox.webapi.common.signed_session import SignedSession
from xbox.webapi.scripts import XAL_TOKENS_FILE


class XALStore(BaseModel):
    """Used to store/load authorization data"""

    signing_key: str
    session_id: str
    live: OAuth2TokenResponse
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
            print(f"Refreshing XAL tokens @ {token_filepath}")
            session.request_signer = RequestSigner.from_pem(store.signing_key)
            xal = XALManager(
                session, store.device_id, store.app_params, store.client_params
            )
            live_token, sisu = await xal.refresh_sisu(
                store.session_id, store.live.refresh_token
            )

            # Store new tokens
            store.live = live_token
            store.sisu = sisu

            # Save refreshed tokens to disk
            with open(token_filepath, mode="w") as f:
                print(f"Finished refreshing, updating tokens at {token_filepath}")
                json.dump(store, f, default=pydantic_encoder)

            sys.exit(0)

        # Do authentication
        xal = XALManager(session, device_id, app_params, client_params)
        session_id, live_response, sisu_response = await xal.auth_flow(
            user_prompt_authentication
        )
        print(
            f"Sisu auth finished:\n\nSESSION-ID={session_id}\n\nLIVE={live_response}\n\nSISU={sisu_response}"
        )

        # Save authorization data
        store = XALStore(
            signing_key=session.request_signer.export_signing_key(),
            session_id=session_id,
            live=live_response,
            sisu=sisu_response,
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
