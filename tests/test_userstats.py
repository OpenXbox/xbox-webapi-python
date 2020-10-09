import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_userstats_by_scid(aresponses, xbl_client):
    aresponses.add("userstats.xboxlive.com", response=get_response("userstats_by_scid"))
    ret = await xbl_client.userstats.get_stats(
        "2669321029139235", "1370999b-fca2-4c53-8ec5-73493bcb67e5"
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.statlistscollection) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_userstats_by_scid_with_metadata(aresponses, xbl_client):
    aresponses.add(
        "userstats.xboxlive.com",
        response=get_response("userstats_by_scid_with_metadata"),
    )
    ret = await xbl_client.userstats.get_stats_with_metadata(
        "2669321029139235", "1370999b-fca2-4c53-8ec5-73493bcb67e5"
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.statlistscollection) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_userstats_batch(aresponses, xbl_client):
    aresponses.add("userstats.xboxlive.com", response=get_response("userstats_batch"))
    ret = await xbl_client.userstats.get_stats_batch(["2584878536129841"], "1717113201")
    await xbl_client._auth_mgr.session.close()

    assert len(ret.statlistscollection) == 1
    assert len(ret.groups) == 1
    assert len(ret.groups[0].statlistscollection) > 0

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_userstats_batch_by_scid(aresponses, xbl_client):
    aresponses.add(
        "userstats.xboxlive.com", response=get_response("userstats_batch_by_scid")
    )
    ret = await xbl_client.userstats.get_stats_batch_by_scid(
        ["2669321029139235"], "1370999b-fca2-4c53-8ec5-73493bcb67e5"
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.statlistscollection) == 1
    assert len(ret.groups) == 1
    assert len(ret.groups[0].statlistscollection) == 0

    aresponses.assert_plan_strictly_followed()
