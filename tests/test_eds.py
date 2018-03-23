from betamax import Betamax
from xbox.webapi.api.provider import eds


def test_get_details(xbl_client):
    with Betamax(xbl_client.session).use_cassette('eds_get_details'):
        ret = xbl_client.eds.get_details(
            ids=["a3807603-9e22-48b2-8b75-c6bf36ddc511",
                 "e0dec6f3-9e8f-4f0c-a93a-acfba29fd890"],
            mediagroup=eds.MediaGroup.GAME_TYPE
        )

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['Items']) == 2


def test_singlemediagroup_search(xbl_client):
    with Betamax(xbl_client.session).use_cassette('eds_singlemediagroup_search'):
        ret = xbl_client.eds.get_singlemediagroup_search(
            search_query='sea',
            max_items=1,
            media_item_types='DGame'
        )

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['Items']) == 1
        assert data['Items'][0]['MediaItemType'] == 'DGame'
        assert data['Items'][0]['MediaGroup'] == 'GameType'
        assert data['Items'][0]['Name'] == 'Sea of Thieves Final Beta'

        assert len(data['Totals']) == 1
        assert data['Totals'][0]['Count'] == 192
        assert data['Totals'][0]['Name'] == 'GameType'


def test_crossmediagroup_search(xbl_client):
    with Betamax(xbl_client.session).use_cassette('eds_crossmediagroup_search'):
        ret = xbl_client.eds.get_crossmediagroup_search(
            search_query='halo',
            max_items=10
        )

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['Items']) == 10
        assert data['Items'][0]['Name'] == 'Halo: Spartan Assault'
        assert data['Items'][0]['ID'] == 'a3807603-9e22-48b2-8b75-c6bf36ddc511'
