from betamax import Betamax


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