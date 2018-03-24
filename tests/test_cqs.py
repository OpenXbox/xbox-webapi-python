from betamax import Betamax


def test_channel_list_download(xbl_client):
    with Betamax(xbl_client.session).use_cassette('cqs_get_channel_list'):
        ret = xbl_client.cqs.get_channel_list(
            locale_info='de-DE',
            headend_id='dbd2530a-fcd5-8ff0-b89d-20cd7e021502'
        )

        assert ret.status_code == 200
        data = ret.json()
        assert len(data['Channels']) == 8

        channel = data['Channels'][0]
        assert channel['ChannelId'] is not None
        assert channel['CallSign'] is not None
        assert channel['ChannelNumber'] is not None
        assert channel['StartDate'] is not None
        assert channel['EndDate'] is not None


def test_schedule_download(xbl_client):
    with Betamax(xbl_client.session).use_cassette('cqs_get_schedule'):
        ret = xbl_client.cqs.get_schedule(
            locale_info='de-DE',
            headend_id='dbd2530a-fcd5-8ff0-b89d-20cd7e021502',
            start_date='2018-03-20T23:50:00.000Z',
            duration_minutes=60,
            channel_skip=0,
            channel_count=5
        )

        assert ret.status_code == 200
        data = ret.json()
        assert len(data['Channels']) == 5

        channel_program = data['Channels'][0]['Programs'][0]
        assert channel_program['Name'] is not None
        assert channel_program['MediaItemType'] is not None
        assert channel_program['Id'] is not None
        assert channel_program['StartDate'] is not None
        assert channel_program['EndDate'] is not None
