from bomberman.objects.base import Renderable


class Indestructible(Renderable):
    def __init__(self):
        super(Indestructible, self).__init__('indestructible.png')

    def as_json(self):
        return {'type': 'indestructible', 'position': self.position}
