"""
Xbox Authentication Library

Authenticate with Windows Live Server and Xbox Live (used by mobile Xbox Apps)
"""
import uuid

import httpx

from xbox.webapi.authentication.models import TitleEndpointsResponse, XADResponse
from xbox.webapi.common.signed_session import SignedSession


class XALManager:
    def __init__(self, session: SignedSession):
        self.session = session

    @staticmethod
    async def get_title_endpoints(session: httpx.AsyncClient) -> TitleEndpointsResponse:
        url = "https://title.mgt.xboxlive.com/titles/default/endpoints"
        headers = {"x-xbl-contract-version": "1"}
        params = {"type": 1}
        resp = await session.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return TitleEndpointsResponse(**resp.json())

    async def request_device_token(self, device_id: uuid.UUID) -> XADResponse:
        url = "https://device.auth.xboxlive.com/device/authenticate"
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "ProofOfPossession",
                "Id": str(device_id).upper(),
                "DeviceType": "Win32",
                "Version": "10.0.22000.194",
                "ProofKey": self.session.request_signer.proof_field,
            },
        }

        resp = await self.session.send_signed("POST", url, headers=headers, json=data)
        resp.raise_for_status()
        return XADResponse(**resp.json())
