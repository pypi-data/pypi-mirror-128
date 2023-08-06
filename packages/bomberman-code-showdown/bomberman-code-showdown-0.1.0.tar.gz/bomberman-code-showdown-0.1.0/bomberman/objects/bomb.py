from bomberman.objects.base import Renderable


class Bomb(Renderable):
    def __init__(self, owner):
        super(Bomb, self).__init__('bomb.png')
        self.owner = owner
        self.explosion_range = owner.explosion_range
        self.time_to_explosion = owner.bomb_wait_time

    def as_json(self):
        return {'type': 'bomb', 'position': self.position}

    def due_to_explode(self):
        return self.time_to_explosion <= 0
