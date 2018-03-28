from betamax import Betamax


def test_presence_batch(xbl_client):
    with Betamax(xbl_client.session).use_cassette('presence_batch'):
        ret = xbl_client.presence.get_presence_batch(
            ['2669321029139235', '2584878536129841']
        )

        assert ret.status_code == 200
        data = ret.json()

        assert len(data) == 2
        assert data[0]['xuid'] == '2669321029139235'
        assert data[0]['state'] == 'Offline'

        assert data[1]['xuid'] == '2584878536129841'
        assert data[1]['state'] == 'Offline'


def test_presence_own(xbl_client):
    with Betamax(xbl_client.session).use_cassette('presence_own'):
        ret = xbl_client.presence.get_presence_own()

        assert ret.status_code == 200
        data = ret.json()

        assert data['xuid'] == '2535428504476914'
        assert data['state'] == 'Offline'
