from betamax import Betamax


def test_titlehub_titlehistory(xbl_client):
    with Betamax(xbl_client.session).use_cassette('titlehub_titlehistory'):
        ret = xbl_client.titlehub.get_title_history(987654321)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['titles']) == 5


def test_titlehub_titleinfo(xbl_client):
    with Betamax(xbl_client.session).use_cassette('titlehub_titleinfo'):
        ret = xbl_client.titlehub.get_title_info(1717113201)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['titles']) == 1


def test_titlehub_batch(xbl_client):
    with Betamax(xbl_client.session).use_cassette('titlehub_batch'):
        ret = xbl_client.titlehub.get_titles_batch(
            ['Microsoft.SeaofThieves_8wekyb3d8bbwe', 'Microsoft.XboxApp_8wekyb3d8bbwe']
        )

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['titles']) == 2
