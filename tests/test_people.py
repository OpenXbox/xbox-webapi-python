from betamax import Betamax


def test_people_friends_own(xbl_client):
    with Betamax(xbl_client.session).use_cassette('people_friends_own'):
        ret = xbl_client.people.get_friends_own()

        assert ret.status_code == 200
        data = ret.json()

        assert data['totalCount'] == 2
        assert len(data['people']) == 2


def test_people_summary_by_gamertag(xbl_client):
    with Betamax(xbl_client.session).use_cassette('people_summary_by_gamertag'):
        ret = xbl_client.people.get_friends_summary_by_gamertag('e')

        assert ret.status_code == 200
        data = ret.json()

        assert data['targetFollowingCount'] == 0
        assert data['targetFollowerCount'] == 20991
        assert data['isCallerFollowingTarget'] is False
        assert data['isTargetFollowingCaller'] is False
        assert data['hasCallerMarkedTargetAsFavorite'] is False
        assert data['hasCallerMarkedTargetAsKnown'] is False
        assert data['legacyFriendStatus'] == 'None'


def test_people_summary_by_xuid(xbl_client):
    with Betamax(xbl_client.session).use_cassette('people_summary_by_xuid'):
        ret = xbl_client.people.get_friends_summary_by_xuid('2669321029139235')
        assert ret.status_code == 200
        data = ret.json()

        assert data['targetFollowingCount'] == 0
        assert data['targetFollowerCount'] == 20991
        assert data['isCallerFollowingTarget'] is False
        assert data['isTargetFollowingCaller'] is False
        assert data['hasCallerMarkedTargetAsFavorite'] is False
        assert data['hasCallerMarkedTargetAsKnown'] is False
        assert data['legacyFriendStatus'] == 'None'


def test_people_summary_own(xbl_client):
    with Betamax(xbl_client.session).use_cassette('people_summary_own'):
        ret = xbl_client.people.get_friends_summary_own()

        assert ret.status_code == 200
        data = ret.json()

        assert data['targetFollowingCount'] == 2
        assert data['targetFollowerCount'] == 1
        assert data['isCallerFollowingTarget'] is False
        assert data['isTargetFollowingCaller'] is False
        assert data['hasCallerMarkedTargetAsFavorite'] is False
        assert data['hasCallerMarkedTargetAsKnown'] is False
        assert data['legacyFriendStatus'] == 'None'
        assert data['availablePeopleSlots'] == 998
        assert data['recentChangeCount'] == 1
        assert data['watermark'] == '5248264408914225648'


def test_profiles_batch(xbl_client):
    with Betamax(xbl_client.session).use_cassette('people_batch'):
        ret = xbl_client.people.get_friends_own_batch(
            ['2669321029139235', '2584878536129841']
        )

        assert ret.status_code == 200
        data = ret.json()

        assert data['totalCount'] == 2
        assert len(data['people']) == 2
