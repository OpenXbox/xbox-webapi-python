from betamax import Betamax


def test_profile_by_xuid(xbl_client):
    with Betamax(xbl_client.session).use_cassette('profile_by_xuid'):
        ret = xbl_client.profile.get_profile_by_xuid('2669321029139235')

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['profileUsers']) == 1
        assert data['profileUsers'][0]['id'] == '2669321029139235'


def test_profile_by_gamertag(xbl_client):
    with Betamax(xbl_client.session).use_cassette('profile_by_gamertag'):
        ret = xbl_client.profile.get_profile_by_gamertag('e')

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['profileUsers']) == 1
        assert data['profileUsers'][0]['id'] == '2669321029139235'


def test_profiles_batch(xbl_client):
    with Betamax(xbl_client.session).use_cassette('profile_batch'):
        ret = xbl_client.profile.get_profiles(['2669321029139235', '2584878536129841'])

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['profileUsers']) == 2
