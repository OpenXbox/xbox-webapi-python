from betamax import Betamax


def test_gameclips_recent_xuid(xbl_client):
    with Betamax(xbl_client.session).use_cassette('gameclips_recent_xuid'):
        ret = xbl_client.gameclips.get_recent_clips_by_xuid('2669321029139235', skip_items=0, max_items=25)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['gameClips']) == 25


def test_gameclips_recent_xuid_titleid_filter(xbl_client):
    with Betamax(xbl_client.session).use_cassette('gameclips_recent_xuid_titleid'):
        ret = xbl_client.gameclips.get_recent_clips_by_xuid('2669321029139235', title_id=219630713, skip_items=0, max_items=25)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['gameClips']) == 25


def test_gameclips_recent_own(xbl_client):
    with Betamax(xbl_client.session).use_cassette('gameclips_recent_own'):
        ret = xbl_client.gameclips.get_recent_own_clips(skip_items=0, max_items=25)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['gameClips']) == 25


def test_gameclips_recent_own_titleid_filter(xbl_client):
    with Betamax(xbl_client.session).use_cassette('gameclips_recent_own_titleid'):
        ret = xbl_client.gameclips.get_recent_own_clips(title_id=219630713, skip_items=0, max_items=25)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['gameClips']) == 25


def test_gameclips_recent_community(xbl_client):
    with Betamax(xbl_client.session).use_cassette('gameclips_recent_community'):
        ret = xbl_client.gameclips.get_recent_community_clips_by_title_id('219630713')

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['gameClips']) == 99


def test_gameclips_saved_xuid(xbl_client):
    with Betamax(xbl_client.session).use_cassette('gameclips_saved_xuid'):
        ret = xbl_client.gameclips.get_saved_clips_by_xuid('2669321029139235', skip_items=0, max_items=25)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['gameClips']) == 25


def test_gameclips_saved_xuid_titleid_filter(xbl_client):
    with Betamax(xbl_client.session).use_cassette('gameclips_saved_xuid_titleid'):
        ret = xbl_client.gameclips.get_saved_clips_by_xuid('2669321029139235', title_id=219630713, skip_items=0, max_items=25)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['gameClips']) == 25


def test_gameclips_saved_own(xbl_client):
    with Betamax(xbl_client.session).use_cassette('gameclips_saved_own'):
        ret = xbl_client.gameclips.get_saved_own_clips(skip_items=0, max_items=25)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['gameClips']) == 25


def test_gameclips_saved_own_titleid_filter(xbl_client):
    with Betamax(xbl_client.session).use_cassette('gameclips_saved_own_titleid'):
        ret = xbl_client.gameclips.get_saved_own_clips(title_id=219630713, skip_items=0, max_items=25)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['gameClips']) == 25


def test_gameclips_saved_community(xbl_client):
    with Betamax(xbl_client.session).use_cassette('gameclips_saved_community'):
        ret = xbl_client.gameclips.get_saved_community_clips_by_title_id(219630713)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['gameClips']) == 99
