import os
import pytest

base_path = os.path.dirname(os.path.realpath(__file__))

@pytest.mark.asyncio
async def test_achievement_360_all(aresponses, xbl_client):
    xuid = "2669321029139235"
    title_id = 1297290392
    with open(f"{base_path}/data/responses/achievements_360_all.json", "r") as f:
        response = f.read()
    aresponses.add("achievements.xboxlive.com", response=response)
    
    ret = await xbl_client.achievements.get_achievements_xbox360_all(xuid, title_id)
    
    assert ret.paging_info.total_records == 15
    aresponses.assert_plan_strictly_followed()


# def test_achievement_360_earned(xbl_client):
#     with Betamax(xbl_client.session).use_cassette('achievements_360_earned'):
#         ret = xbl_client.achievements.\
#             get_achievements_xbox360_earned('2669321029139235', 1297290392)

#         assert ret.status_code == 200
#         data = ret.json()

#         assert len(data['achievements']) == 1


# def test_achievement_360_recent_progress(xbl_client):
#     with Betamax(xbl_client.session).use_cassette('achievements_360_recent_progress'):
#         ret = xbl_client.achievements.\
#             get_achievements_xbox360_recent_progress_and_info(xuid='2669321029139235')

#         assert ret.status_code == 200
#         data = ret.json()

#         assert len(data['titles']) == 32


# def test_achievement_one_details(xbl_client):
#     with Betamax(xbl_client.session).use_cassette('achievements_one_details'):
#         ret = xbl_client.achievements.\
#             get_achievements_detail_item(xuid='2669321029139235',
#                                          service_config_id='1370999b-fca2-4c53-8ec5-73493bcb67e5',
#                                          achievement_id='39')

#         assert ret.status_code == 200
#         data = ret.json()

#         assert len(data['achievements']) == 1


# def test_achievement_one_gameprogress(xbl_client):
#     with Betamax(xbl_client.session).use_cassette('achievements_one_gameprogress'):
#         ret = xbl_client.achievements.\
#             get_achievements_xboxone_gameprogress(xuid='2669321029139235', title_id=219630713)

#         assert ret.status_code == 200
#         data = ret.json()

#         assert len(data['achievements']) == 32


# def test_achievement_one_recent_progress(xbl_client):
#     with Betamax(xbl_client.session).use_cassette('achievements_one_recent_progress'):
#         ret = xbl_client.achievements.\
#             get_achievements_xboxone_recent_progress_and_info(xuid='2669321029139235')

#         assert ret.status_code == 200
#         data = ret.json()

#         assert len(data['titles']) == 32
