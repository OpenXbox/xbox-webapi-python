"""Authentication Models."""
from datetime import datetime, timedelta, timezone
from typing import Dict, List

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
    refresh_token: str
    user_id: str
    issued: datetime = Field(default_factory=utc_now)

    def is_valid(self) -> bool:
        return (self.issued + timedelta(seconds=self.expires_in)) > utc_now()
