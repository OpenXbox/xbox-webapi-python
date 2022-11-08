from httpx import Response
import pytest

from xbox.webapi.api.provider.catalog.models import AlternateIdType, FieldsTemplate

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_get_products(respx_mock, xbl_client):
    route = respx_mock.get("https://displaycatalog.mp.microsoft.com").mock(
        return_value=Response(200, json=get_response_json("catalog_browse"))
    )
    ret = await xbl_client.catalog.get_products(["C5DTJ99626K3", "BT5P2X999VH2"])

    assert len(ret.products) == 2
    assert route.called


@pytest.mark.asyncio
async def test_get_products_detail(respx_mock, xbl_client):
    route = respx_mock.get("https://displaycatalog.mp.microsoft.com").mock(
        return_value=Response(200, json=get_response_json("catalog_browse_details"))
    )

    ret = await xbl_client.catalog.get_products(
        ["C5DTJ99626K3", "BT5P2X999VH2"], fields=FieldsTemplate.DETAILS
    )

    assert len(ret.products) == 2
    assert route.called


@pytest.mark.asyncio
async def test_get_product_from_alternate_id(respx_mock, xbl_client):
    route = respx_mock.get("https://displaycatalog.mp.microsoft.com").mock(
        return_value=Response(200, json=get_response_json("catalog_product_lookup"))
    )
    ret = await xbl_client.catalog.get_product_from_alternate_id(
        "4DF9E0F8.Netflix_mcm4njqhnhss8", AlternateIdType.PACKAGE_FAMILY_NAME
    )

    assert ret.total_result_count == 1
    assert route.called


@pytest.mark.asyncio
async def test_get_product_from_alternate_id_legacy(respx_mock, xbl_client):
    route = respx_mock.get("https://displaycatalog.mp.microsoft.com").mock(
        return_value=Response(
            200, json=get_response_json("catalog_product_lookup_legacy")
        )
    )
    ret = await xbl_client.catalog.get_product_from_alternate_id(
        "71e7df12-89e0-4dc7-a5ff-a182fc2df94f", AlternateIdType.LEGACY_XBOX_PRODUCT_ID
    )

    assert ret.total_result_count == 1
    assert route.called


@pytest.mark.asyncio
async def test_product_search(respx_mock, xbl_client):
    route = respx_mock.get("https://displaycatalog.mp.microsoft.com").mock(
        return_value=Response(200, json=get_response_json("catalog_search"))
    )
    ret = await xbl_client.catalog.product_search("dest")

    assert ret.total_result_count == 10
    assert route.called
