"""
Store Catalog - Lookup Product Information
"""
from typing import List

from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.catalog.models import (
    AlternateIdType,
    CatalogResponse,
    CatalogSearchResponse,
    FieldsTemplate,
    PlatformType,
)


class CatalogProvider(BaseProvider):
    CATALOG_URL = "https://displaycatalog.mp.microsoft.com"
    SEPERATOR = ","

    async def get_products(
        self, big_ids: List[str], fields: FieldsTemplate = FieldsTemplate.DETAILS
    ) -> CatalogResponse:
        """Lookup product by Big IDs."""
        ids = self.SEPERATOR.join(big_ids)
        params = {
            "actionFilter": "Browse",
            "bigIds": ids,
            "fieldsTemplate": fields,
            "languages": self.client.language.locale,
            "market": self.client.language.short_id,
        }
        url = f"{self.CATALOG_URL}/v7.0/products"
        resp = await self.client.session.get(url, params=params, include_auth=False)
        resp.raise_for_status()
        return CatalogResponse.parse_raw(await resp.text())

    async def get_product_from_alternate_id(
        self,
        id: str,
        id_type: AlternateIdType,
        fields: FieldsTemplate = FieldsTemplate.DETAILS,
        top: int = 25,
    ) -> CatalogResponse:
        """Lookup product by Alternate ID."""
        params = {
            "top": top,
            "alternateId": id_type.value,
            "fieldsTemplate": fields,
            "languages": self.client.language.locale,
            "market": self.client.language.short_id,
            "value": id,
        }
        url = f"{self.CATALOG_URL}/v7.0/products/lookup"
        resp = await self.client.session.get(url, params=params, include_auth=False)
        resp.raise_for_status()
        return CatalogResponse.parse_raw(await resp.text())

    async def product_search(
        self, query: str, platform: PlatformType = PlatformType.XBOX, top: int = 5
    ) -> CatalogSearchResponse:
        """Search for products by name."""
        params = {
            "languages": self.client.language.locale,
            "market": self.client.language.short_id,
            "platformdependencyname": platform.value,
            "productFamilyNames": "Games,Apps",
            "query": query,
            "topProducts": top,
        }
        url = f"{self.CATALOG_URL}/v7.0/productFamilies/autosuggest"
        resp = await self.client.session.get(url, params=params, include_auth=False)
        resp.raise_for_status()
        return CatalogSearchResponse.parse_raw(await resp.text())
