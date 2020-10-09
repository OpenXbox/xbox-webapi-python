"""
Signed Session

A wrapper around httpx' AsyncClient which transparently calculates the "Signature" header.
"""

import aiohttp

from xbox.webapi.common.request_signer import RequestSigner


class SignedSession(aiohttp.ClientSession):
    def __init__(self, request_signer=None):
        super().__init__()
        self.request_signer = request_signer or RequestSigner()

    @classmethod
    def from_pem_signing_key(cls, pem_string: str):
        request_signer = RequestSigner.from_pem(pem_string)
        return cls(request_signer)

    async def prepare_signed_request(
        self, request: aiohttp.ClientRequest
    ) -> aiohttp.ClientRequest:
        path_and_query = request.url.raw_path.decode()
        authorization = request.headers.get("Authorization", "")

        body = request.body

        signature = self.request_signer.sign(
            method=request.method,
            path_and_query=path_and_query,
            body=body,
            authorization=authorization,
        )

        request.headers["Signature"] = signature
        return request
