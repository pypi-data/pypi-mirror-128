class PlayerStats:
    def __init__(self, player):
        self.player = player
        self._bombs_placed = 0
        self._powerups_bombs = 0
        self._powerups_fire = 0
        self._powerups_speed = 0
        self._max_bombs_at_the_same_time = 0
        self._walls_destroyed = 0
        self._powerups_destroyed = 0

    def incr_bombs_placed(self):
        self._bombs_placed += 1

    def incr_powerup_pickup(self, powerup_id: str):
        from bomberman.objects.powerup import SpeedPowerUp, MoreBombsPowerUp, BiggerExplosionPowerUp

        if powerup_id == MoreBombsPowerUp.power_up_id:
            self._powerups_bombs += 1
        elif powerup_id == BiggerExplosionPowerUp.power_up_id:
            self._powerups_fire += 1
        elif powerup_id == SpeedPowerUp.power_up_id:
            self._powerups_speed += 1

    def destructible_destroyed(self, destr):
        from bomberman.objects.powerup import BasePowerUp
        if isinstance(destr, BasePowerUp):
            self._powerups_destroyed += 1
        else:
            self._walls_destroyed += 1

    def record_bomb_count(self):
        if self.player.current_bombs > self._max_bombs_at_the_same_time:
            self._max_bombs_at_the_same_time = self.player.current_bombs

    def to_json(self):
        return {
            'player': self.player.name,
            'bombs_placed': self._bombs_placed,
            'powerups': {
                'bombs': self._powerups_bombs,
                'explosion': self._powerups_fire,
                'speed': self._powerups_speed
            },
            'walls_destroyed': self._walls_destroyed,
            'powerups_destroyed': self._powerups_destroyed,
            'max_bomb_count': self._max_bombs_at_the_same_time
        }
