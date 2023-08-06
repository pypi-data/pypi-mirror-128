from bomberman.pygame_utils import load_image_from_resource


class Renderable:
    def __init__(self, image):
        self.position = None
        self.image = load_image_from_resource('bomberman.objects', image)
