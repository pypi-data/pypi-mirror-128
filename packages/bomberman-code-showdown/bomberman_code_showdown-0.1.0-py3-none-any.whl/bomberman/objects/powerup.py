from bomberman.objects.destructible import Destructible
from bomberman.objects.player import Player


class BasePowerUp(Destructible):
    power_up_id = None
    player_can_move_over = True

    def apply(self, player: Player):
        pass

    def as_json(self):
        return {'type': self.power_up_id}


class MoreBombsPowerUp(BasePowerUp):
    power_up_id = 'more_bombs'

    def __init__(self):
        super(MoreBombsPowerUp, self).__init__('powerup_more_bombs.png')

    def apply(self, player: Player):
        player.max_bombs += 1


class BiggerExplosionPowerUp(BasePowerUp):
    power_up_id = 'bigger_explosion'

    def __init__(self):
        super(BiggerExplosionPowerUp, self).__init__('powerup_bigger_explosion.png')

    def apply(self, player: Player):
        player.explosion_range += 1


class SpeedPowerUp(BasePowerUp):
    power_up_id = 'speed'

    def __init__(self):
        super(SpeedPowerUp, self).__init__('powerup_speed.png')

    def apply(self, player: Player):
        player.speed += 1
