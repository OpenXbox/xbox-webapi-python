import pytest

from xbox.webapi.api.provider.catalog.models import AlternateIdType, FieldsTemplate

from tests.common import get_response


@pytest.mark.asyncio
async def test_get_products(aresponses, xbl_client):
    aresponses.add(
        "displaycatalog.mp.microsoft.com", response=get_response("catalog_browse")
    )
    ret = await xbl_client.catalog.get_products(["C5DTJ99626K3", "BT5P2X999VH2"])
    await xbl_client._auth_mgr.session.close()

    assert len(ret.products) == 2
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_products_detail(aresponses, xbl_client):
    aresponses.add(
        "displaycatalog.mp.microsoft.com",
        response=get_response("catalog_browse_details"),
    )
    ret = await xbl_client.catalog.get_products(
        ["C5DTJ99626K3", "BT5P2X999VH2"], fields=FieldsTemplate.DETAILS
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.products) == 2
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_product_from_alternate_id(aresponses, xbl_client):
    aresponses.add(
        "displaycatalog.mp.microsoft.com",
        response=get_response("catalog_product_lookup"),
    )
    ret = await xbl_client.catalog.get_product_from_alternate_id(
        "4DF9E0F8.Netflix_mcm4njqhnhss8", AlternateIdType.PACKAGE_FAMILY_NAME
    )
    await xbl_client._auth_mgr.session.close()

    assert ret.total_result_count == 1
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_product_search(aresponses, xbl_client):
    aresponses.add(
        "displaycatalog.mp.microsoft.com", response=get_response("catalog_search")
    )
    ret = await xbl_client.catalog.product_search("dest")
    await xbl_client._auth_mgr.session.close()

    assert ret.total_result_count == 10
    aresponses.assert_plan_strictly_followed()
