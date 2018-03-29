from betamax import Betamax


def test_userstats_by_scid(xbl_client):
    with Betamax(xbl_client.session).use_cassette('userstats_by_scid'):
        ret = xbl_client.userstats.get_stats('2669321029139235', '1370999b-fca2-4c53-8ec5-73493bcb67e5')

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['statlistscollection']) == 1
        stat = data['statlistscollection'][0]['stats'][0]

        assert stat['type'] == 'Integer'
        assert stat['name'] == 'MinutesPlayed'
        assert stat['xuid'] == '2669321029139235'
        assert stat['value'] == '1220'
        assert stat['scid'] == '1370999b-fca2-4c53-8ec5-73493bcb67e5'


def test_userstats_by_scid_with_metadata(xbl_client):
    with Betamax(xbl_client.session).use_cassette('userstats_by_scid_with_metadata'):
        ret = xbl_client.userstats.get_stats_with_metadata('2669321029139235', '1370999b-fca2-4c53-8ec5-73493bcb67e5')

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['statlistscollection']) == 1
        stat = data['statlistscollection'][0]['stats'][0]

        assert stat['type'] == 'Integer'
        assert stat['name'] == 'MinutesPlayed'
        assert stat['xuid'] == '2669321029139235'
        assert stat['value'] == '1220'
        assert stat['scid'] == '1370999b-fca2-4c53-8ec5-73493bcb67e5'


def test_userstats_batch(xbl_client):
    with Betamax(xbl_client.session).use_cassette('userstats_batch'):
        ret = xbl_client.userstats.get_stats_batch(['2584878536129841'], 1717113201)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['statlistscollection']) == 1
        assert len(data['groups']) == 1

        stat = data['groups'][0]['statlistscollection'][0]['stats'][0]

        assert stat['type'] == 'Double'
        assert stat['name'] == 'ChestsCashedIn'
        assert stat['xuid'] == '2584878536129841'
        assert stat['value'] == '5'
        assert stat['scid'] == '00000000-0000-0000-0000-000066591171'


def test_userstats_batch_by_scid(xbl_client):
    with Betamax(xbl_client.session).use_cassette('userstats_batch_by_scid'):
        ret = xbl_client.userstats.get_stats_batch_by_scid(['2669321029139235'], '1370999b-fca2-4c53-8ec5-73493bcb67e5')

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['statlistscollection']) == 1
        stat = data['statlistscollection'][0]['stats'][0]

        assert stat['type'] == 'Integer'
        assert stat['name'] == 'MinutesPlayed'
        assert stat['xuid'] == '2669321029139235'
        assert stat['value'] == '1220'
        assert stat['scid'] == '1370999b-fca2-4c53-8ec5-73493bcb67e5'
