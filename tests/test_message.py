from betamax import Betamax


def test_message_get_inbox(xbl_client):
    with Betamax(xbl_client.session).use_cassette('message_get_message_inbox'):
        ret = xbl_client.message.get_message_inbox(skip_items=0, max_items=100)

        assert ret.status_code == 200
        data = ret.json()

        assert len(data['results']) == 1
        result = data['results'][0]
        header = result['header']
        assert result['messageSummary'] == 'Test message string'
        assert header['id'] == '1'
        assert header['isRead'] is False
        assert header['hasText'] is True
        assert header['sent'] == '2018-03-28T14:15:18Z'
        assert header['expiration'] == '2018-04-27T14:15:18Z'
        assert header['messageType'] == 'User'
        assert header['sender'] == 'NoExist1'
        assert header['senderXuid'] == 1234567890123456


def test_message_get_message(xbl_client):
    with Betamax(xbl_client.session).use_cassette('message_get_message'):
        ret = xbl_client.message.get_message('1')

        assert ret.status_code == 200
        data = ret.json()

        header = data['header']
        assert data['attachmentId'] is None
        assert data['attachment'] is None
        assert data['messageText'] == 'Test message string, up to 256 characters'

        assert header['hasText'] is True
        assert header['sent'] == '2018-03-28T14:15:18Z'
        assert header['expiration'] == '2018-04-27T14:15:18Z'
        assert header['messageType'] == 'User'
        assert header['sender'] == 'NoExist1'
        assert header['senderXuid'] == 1234567890123456


def test_message_delete_msg(xbl_client):
    with Betamax(xbl_client.session).use_cassette('message_delete_message'):
        ret = xbl_client.message.delete_message('1')

        assert ret.status_code == 204


def test_message_send(xbl_client):
    with Betamax(xbl_client.session).use_cassette('message_send_message'):
        ret = xbl_client.message.send_message(
            message_text='Test string',
            gamertags=['NoExist1', 'NoExist2']
        )

        assert ret.status_code == 200
