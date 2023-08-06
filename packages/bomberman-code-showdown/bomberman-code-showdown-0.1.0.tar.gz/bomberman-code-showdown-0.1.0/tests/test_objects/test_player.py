import pytest

from bomberman.objects.player import Player


@pytest.mark.parametrize('last_action, time_time, expected', [
    (None, 100, 99999),
])
def test_time_since_last_action(last_action, time_time, expected, mocker):
    p = Player('test', 'red')
    p.last_action = last_action
    mocker.patch('time.time', return_value=time_time)
    assert p.time_since_last_action() == expected
