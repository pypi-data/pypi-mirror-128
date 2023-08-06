import time

from bomberman.objects.base import Renderable
from bomberman.pygame_utils import load_image_from_resource
from bomberman.stats import PlayerStats


class Player(Renderable):
    def __init__(self, name, color):
        self.name = name
        self.last_action = None
        super(Player, self).__init__(f'player_{color}.png')
        self._dead_sprite = load_image_from_resource('bomberman.objects', f'player_{color}_dead.png')

        self.speed = 1
        self.current_bombs = 0
        self.max_bombs = 1
        self.explosion_range = 2
        self.bomb_wait_time = 3

        self._movement_disabled = False
        self._is_dead = False

        self.stats = PlayerStats(self)

    def time_since_last_action(self) -> float:
        if not self.last_action:
            return 99999
        return time.time() - self.last_action

    def can_move(self) -> bool:
        return self.time_since_last_action() >= self._get_speed_interval()

    def _get_speed_interval(self) -> float:
        """How often the player can move, given its current speed"""
        return max(0.5 - 0.05 * self.speed, 0.1)

    def reset_action_timer(self):
        self.last_action = time.time()

    def as_json(self, is_me=False):
        return {'type': 'player', 'position': self.position, 'name': self.name, 'is_me': is_me}

    def get_complete_json(self):
        return {
            'name': self.name,
            'position': self.position,
            'max_bombs': self.max_bombs,
            'speed': 1 / self.speed,
            'current_bombs': self.current_bombs,
            'explosion_range': self.explosion_range,
            'bomb_wait_time': self.bomb_wait_time
        }

    def has_bombs_left(self):
        return self.current_bombs < self.max_bombs

    def is_movement_disabled(self):
        return self._movement_disabled

    def disabled_movement(self):
        self._movement_disabled = True

    def _change_to_death_sprite(self):
        self._dead_sprite, self.image = self.image, self._dead_sprite

    def is_dead(self):
        return self._is_dead

    def kill(self):
        self._is_dead = True
        self._movement_disabled = True
        self._change_to_death_sprite()
