"""
Signed Session
A wrapper around httpx' AsyncClient which transparently calculates the "Signature" header.
"""

import httpx

from xbox.webapi.common.request_signer import RequestSigner


class SignedSession(httpx.AsyncClient):
    def __init__(self, request_signer=None):
        super().__init__()
        self.request_signer = request_signer or RequestSigner()

    @classmethod
    def from_pem_signing_key(cls, pem_string: str):
        request_signer = RequestSigner.from_pem(pem_string)
        return cls(request_signer)

    def _prepare_signed_request(self, request: httpx.Request) -> httpx.Request:
        path_and_query = request.url.raw_path.decode()
        authorization = request.headers.get("Authorization", "")

        body = b""
        for byte in request.stream:
            body += byte

        signature = self.request_signer.sign(
            method=request.method,
            path_and_query=path_and_query,
            body=body,
            authorization=authorization,
        )

        request.headers["Signature"] = signature
        return request

    async def send_request_signed(self, request: httpx.Request) -> httpx.Response:
        """
        Shorthand for prepare signed + send
        """
        prepared = self._prepare_signed_request(request)
        return await self.send(prepared)

    async def send_signed(self, method: str, url: str, **kwargs):
        """
        Shorthand for creating request + prepare signed + send
        """
        request = httpx.Request(method, url, **kwargs)
        prepared = self._prepare_signed_request(request)
        return await self.send(prepared)
