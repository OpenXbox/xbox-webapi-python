"""
Example scripts that performs XBL authentication
"""
import argparse
import asyncio
import http.server
import os
import queue
import socketserver
import threading
from urllib.parse import parse_qs, urlparse
import webbrowser

from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse
from xbox.webapi.common.signed_session import SignedSession
from xbox.webapi.scripts import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, TOKENS_FILE

QUEUE = queue.Queue(1)


class AuthCallbackRequestHandler(http.server.BaseHTTPRequestHandler):
    """
    Handles the auth callback that's received when Windows Live auth flow completed
    """

    def do_GET(self):
        try:
            url_path = self.requestline.split(" ")[1]
            query_params = parse_qs(urlparse(url_path).query)
        except Exception as e:
            self.send_error(
                400,
                explain=f"Invalid request='{self.requestline}' - Failed to parse URL Path, error={e}",
            )
            self.end_headers()
            return

        if query_params.get("error"):
            error_description = query_params.get("error_description")
            self.send_error(
                400, explain=f"Auth callback failed - Error: {error_description}"
            )
            self.end_headers()
            return

        auth_code = query_params.get("code")
        if not auth_code:
            self.send_error(
                400,
                explain=f"Auth callback failed - No code received - Original request: {self.requestline}",
            )
            self.end_headers()
            return

        if isinstance(auth_code, list):
            auth_code = auth_code[0]
        elif isinstance(auth_code, str):
            pass
        else:
            raise Exception(f"Invalid code query param: {auth_code}")

        # Put auth_code into queue for do_auth to receive
        QUEUE.put(auth_code)
        response_body = b"<script>window.close()</script>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)


async def do_auth(
    client_id: str, client_secret: str, redirect_uri: str, token_filepath: str
):
    async with SignedSession() as session:
        auth_mgr = AuthenticationManager(
            session, client_id, client_secret, redirect_uri
        )

        # Refresh tokens if we have them
        if os.path.exists(token_filepath):
            with open(token_filepath) as f:
                tokens = f.read()
            auth_mgr.oauth = OAuth2TokenResponse.model_validate_json(tokens)
            await auth_mgr.refresh_tokens()

        # Request new ones if they are not valid
        if not (auth_mgr.xsts_token and auth_mgr.xsts_token.is_valid()):
            auth_url = auth_mgr.generate_authorization_url()
            webbrowser.open(auth_url)
            # Wait for auth code from http server thread
            code = QUEUE.get()
            await auth_mgr.request_tokens(code)

        with open(token_filepath, mode="w") as f:
            print(f"Finished authentication, writing tokens to {token_filepath}")
            f.write(auth_mgr.oauth.json())


async def async_main():
    parser = argparse.ArgumentParser(description="Authenticate with XBL")
    parser.add_argument(
        "--tokens",
        "-t",
        default=TOKENS_FILE,
        help=f"Token filepath. Default: '{TOKENS_FILE}'",
    )
    parser.add_argument(
        "--client-id",
        "-cid",
        default=os.environ.get("CLIENT_ID", CLIENT_ID),
        help="OAuth2 Client ID",
    )
    parser.add_argument(
        "--client-secret",
        "-cs",
        default=os.environ.get("CLIENT_SECRET", CLIENT_SECRET),
        help="OAuth2 Client Secret",
    )
    parser.add_argument(
        "--redirect-uri",
        "-ru",
        default=os.environ.get("REDIRECT_URI", REDIRECT_URI),
        help="OAuth2 Redirect URI",
    )
    parser.add_argument(
        "--port",
        "-p",
        default=8080,
        type=int,
        help="""
        HTTP Server port for awaiting auth callback
        * NOTE: Changing this will break default auth flow and requires providing own OAUTH parameters
        """,
    )
    args = parser.parse_args()

    with socketserver.TCPServer(
        ("0.0.0.0", args.port), AuthCallbackRequestHandler
    ) as httpd:
        print(f"Serving HTTP Server for auth callback at port {args.port}")
        server_thread = threading.Thread(target=httpd.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

        await do_auth(
            args.client_id, args.client_secret, args.redirect_uri, args.tokens
        )


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
