from bomberman.objects.base import Renderable


class Destructible(Renderable):
    player_can_move_over = False

    def __init__(self, image=None):
        super(Destructible, self).__init__(image or 'destructible.png')

    def as_json(self):
        return {'type': 'destructible', 'position': self.position}
