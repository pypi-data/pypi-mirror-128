import io

import pkg_resources
import pygame


def load_image_from_resource(pkg, resource_name):
    image_buffer = pkg_resources.resource_string(pkg, resource_name)
    return pygame.image.load(io.BytesIO(image_buffer))
