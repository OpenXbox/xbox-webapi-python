"""Authentication Models."""
from pydantic import BaseModel
from typing import Dict, List

def to_pascal(string):
    return string.replace("_", " ").title().replace(" ", "")

class XTokenResponse(BaseModel):
    issue_instant: str
    not_after: str
    token: str
    
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_pascal


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
        return f'XBL3.0 x={self.userhash};{self.token}'


class OAuth2TokenResponse(BaseModel):
    token_type: str
    expires_in: int
    scope: str
    access_token: str
    refresh_token: str
    user_id: str
