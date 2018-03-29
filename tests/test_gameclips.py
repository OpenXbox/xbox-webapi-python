from betamax import Betamax


def test_gameclips_xuid(xbl_client):
    with Betamax(xbl_client.session).use_cassette('gameclips_clips_xuid'):
        ret = xbl_client.gameclips.get_recent_clips_by_xuid('2669321029139235', skip_items=0, max_items=25)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['gameClips']) == 25


def test_gameclips_own_clips(xbl_client):
    with Betamax(xbl_client.session).use_cassette('gameclips_own_clips'):
        ret = xbl_client.gameclips.get_recent_own_clips(skip_items=0, max_items=25)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['gameClips']) == 0


def test_gameclips_community_title_id(xbl_client):
    with Betamax(xbl_client.session).use_cassette('gameclips_community_title_id'):
        ret = xbl_client.gameclips.get_recent_community_clips_by_title_id(219630713)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['gameClips']) == 99
