"""Authentication Models."""
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from xbox.webapi.common.models import PascalCaseModel


def utc_now():
    return datetime.now(timezone.utc)


class XTokenResponse(PascalCaseModel):
    issue_instant: datetime
    not_after: datetime
    token: str

    def is_valid(self) -> bool:
        return self.not_after > utc_now()


class XADDisplayClaims(BaseModel):
    # {"xdi": {"did": "F.....", "dcs": "0"}}
    xdi: Dict[str, str]


class XADResponse(XTokenResponse):
    display_claims: XADDisplayClaims


class XATDisplayClaims(BaseModel):
    xti: Dict[str, str]


class XATResponse(XTokenResponse):
    display_claims: XATDisplayClaims


class XAUDisplayClaims(BaseModel):
    xui: List[Dict[str, str]]


class XAUResponse(XTokenResponse):
    display_claims: XAUDisplayClaims


class XSTSDisplayClaims(BaseModel):
    xui: List[Dict[str, str]]


class XSTSResponse(XTokenResponse):
    display_claims: XSTSDisplayClaims

    @property
    def xuid(self) -> str:
        return self.display_claims.xui[0]["xid"]

    @property
    def userhash(self) -> str:
        return self.display_claims.xui[0]["uhs"]

    @property
    def gamertag(self) -> str:
        return self.display_claims.xui[0]["gtg"]

    @property
    def age_group(self) -> str:
        return self.display_claims.xui[0]["agg"]

    @property
    def privileges(self) -> str:
        return self.display_claims.xui[0]["prv"]

    @property
    def user_privileges(self) -> str:
        return self.display_claims.xui[0]["usr"]

    @property
    def authorization_header_value(self) -> str:
        return f"XBL3.0 x={self.userhash};{self.token}"


class OAuth2TokenResponse(BaseModel):
    token_type: str
    expires_in: int
    scope: str
    access_token: str
    refresh_token: Optional[str]
    user_id: str
    issued: datetime = Field(default_factory=utc_now)

    def is_valid(self) -> bool:
        return (self.issued + timedelta(seconds=self.expires_in)) > utc_now()


"""Signature related models"""


class TitleEndpoint(PascalCaseModel):
    protocol: str
    host: str
    host_type: str
    path: Optional[str]
    relying_party: Optional[str]
    sub_relying_party: Optional[str]
    token_type: Optional[str]
    signature_policy_index: Optional[int]
    server_cert_index: Optional[List[int]]


class SignaturePolicy(PascalCaseModel):
    version: int
    supported_algorithms: List[str]
    max_body_bytes: int


class TitleEndpointCertificate(PascalCaseModel):
    thumbprint: str
    is_issuer: Optional[bool]
    root_cert_index: int


class TitleEndpointsResponse(PascalCaseModel):
    end_points: List[TitleEndpoint]
    signature_policies: List[SignaturePolicy]
    certs: List[TitleEndpointCertificate]
    root_certs: List[str]
