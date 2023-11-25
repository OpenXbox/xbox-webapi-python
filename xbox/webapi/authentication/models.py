"""Authentication Models."""
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

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
    refresh_token: Optional[str] = None
    user_id: str
    issued: datetime = Field(default_factory=utc_now)

    def is_valid(self) -> bool:
        return (self.issued + timedelta(seconds=self.expires_in)) > utc_now()


"""XAL related models"""


@dataclass
class XalAppParameters:
    app_id: str
    title_id: str
    redirect_uri: str


@dataclass
class XalClientParameters:
    user_agent: str
    device_type: str
    client_version: str
    query_display: str


class SisuAuthenticationResponse(PascalCaseModel):
    msa_oauth_redirect: str
    msa_request_parameters: Dict[str, str]


class SisuAuthorizationResponse(PascalCaseModel):
    device_token: str
    title_token: XATResponse
    user_token: XAUResponse
    authorization_token: XSTSResponse
    web_page: str
    sandbox: str
    use_modern_gamertag: Optional[bool] = None


"""Signature related models"""


class TitleEndpoint(PascalCaseModel):
    protocol: str
    host: str
    host_type: str
    path: Optional[str] = None
    relying_party: Optional[str] = None
    sub_relying_party: Optional[str] = None
    token_type: Optional[str] = None
    signature_policy_index: Optional[int] = None
    server_cert_index: Optional[List[int]] = None


class SignaturePolicy(PascalCaseModel):
    version: int
    supported_algorithms: List[str]
    max_body_bytes: int


class TitleEndpointCertificate(PascalCaseModel):
    thumbprint: str
    is_issuer: Optional[bool] = None
    root_cert_index: int


class TitleEndpointsResponse(PascalCaseModel):
    end_points: List[TitleEndpoint]
    signature_policies: List[SignaturePolicy]
    certs: List[TitleEndpointCertificate]
    root_certs: List[str]
