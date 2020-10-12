"""Web API Constants."""
from xbox.webapi.api.provider.catalog.models import AlternateIdType

HOME_APP_IDS = {
    AlternateIdType.LEGACY_XBOX_PRODUCT_ID: "7b3ca835-5ef5-4d96-bc84-c1d8b5084236",
    AlternateIdType.XBOX_TITLE_ID: "750323071",
}

SYSTEM_PFN_ID_MAP = {
    "Microsoft.Xbox.LiveTV_8wekyb3d8bbwe": {
        AlternateIdType.LEGACY_XBOX_PRODUCT_ID: "71e7df12-89e0-4dc7-a5ff-a182fc2df94f",
        AlternateIdType.XBOX_TITLE_ID: "371594669",
    },
}
