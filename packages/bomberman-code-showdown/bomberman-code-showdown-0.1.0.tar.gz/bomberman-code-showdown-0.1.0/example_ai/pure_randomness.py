import random
import sys
import time
from urllib.parse import urljoin

import requests

address = sys.argv[1]
ACTION_URL = urljoin(address, 'action')
STATE_URL = urljoin(address, 'game-state')


def ai():
    if random.random() < 0.75:
        direction = random.choice(['up', 'left', 'right', 'down'])
        print(requests.post(ACTION_URL, json={'action': 'move', 'direction': direction}).json())
    else:
        print(requests.post(ACTION_URL, json={'action': 'bomb'}).json())
    time.sleep(0.1)
    print('======')


while True:
    try:
        ai()
    except requests.ConnectionError:
        print('Waiting to start')
        pass
