from typing import Union

from bomberman.objects.base import Renderable
from bomberman.objects.bomb import Bomb
from bomberman.objects.player import Player


class Fire(Renderable):
    def __init__(self):
        super(Fire, self).__init__('fire.png')
        self.ttl = 1

    def hits(self, target: Union[Player, Bomb]):
        return tuple(self.position) == tuple(target.position)

    def as_json(self):
        return {'type': 'fire', 'position': self.position}
