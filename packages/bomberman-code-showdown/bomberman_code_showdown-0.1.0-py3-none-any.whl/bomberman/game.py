import queue
import random
import time
from typing import List, Optional

import pygame.event
from pygame import Vector2

from bomberman.events import EVENT_PLAYER_1, EVENT_PLAYER_2, EVENT_PLAYER_3, EVENT_PLAYER_4, ALL_PLAYER_EVENT_TYPES
from bomberman.objects.bomb import Bomb
from bomberman.objects.destructible import Destructible
from bomberman.objects.fire import Fire
from bomberman.objects.indestructible import Indestructible
from bomberman.objects.player import Player
from bomberman.objects.powerup import SpeedPowerUp, BiggerExplosionPowerUp, MoreBombsPowerUp, BasePowerUp


def get_destructible_at(row, col, game_state) -> Optional[Destructible]:
    for thing in game_state[row][col]:
        if isinstance(thing, Destructible):
            return thing


def slot_is_indestructible(row, col, game_state):
    return slot_is(row, col, game_state, Indestructible)


def slot_is_bomb(row, col, game_state):
    return slot_is(row, col, game_state, Bomb)


def slot_is(row, col, game_state, type) -> bool:
    return bool(game_state[row][col]) and any(isinstance(x, type) for x in game_state[row][col])


def player_can_move_into(game_state, position):
    args = position[0], position[1], game_state

    destructible = get_destructible_at(*args)
    if destructible:
        can_move_into_destructible = destructible.player_can_move_over
    else:
        can_move_into_destructible = True  # no destructible

    return (not slot_is_indestructible(*args)) and can_move_into_destructible and (not slot_is_bomb(*args))


def get_cell_in_direction(reference, direction, distance=1):
    if direction == 'up':
        return [reference[0] - distance, reference[1]]
    elif direction == 'down':
        return [reference[0] + distance, reference[1]]
    elif direction == 'left':
        return [reference[0], reference[1] - distance]
    elif direction == 'right':
        return [reference[0], reference[1] + distance]


class BombermanGame:
    POWERUP_CLASSES = [
        SpeedPowerUp,
        MoreBombsPowerUp,
        BiggerExplosionPowerUp,
    ]

    def __init__(self, players: List[Player], map_size: Vector2 = Vector2(11, 11)):
        self.players = players
        self.game_state = self.create_initial_game_state(map_size)
        self.remote_queue = queue.Queue()
        self.bombs = []
        self.fires = []

        self.timer = 120
        self.finished = False
        self.winner = None

        self._last_update = time.time()

    def create_initial_game_state(self, game_size: Vector2):
        game_state = []
        empty_spots = []

        height = int(game_size.x)
        width = int(game_size.y)

        for row in range(height):
            game_state.append([])
            for col in range(width):
                game_state[row].append([])

                if row % 2 == 1 and col % 2 == 1:
                    game_state[row][col].append(Indestructible())
                    game_state[row][col][0].position = (row, col)

                if not game_state[row][col]:
                    empty_spots.append((row, col))

        random.shuffle(empty_spots)
        for _ in range(round(height * width * 0.5)):
            pos = empty_spots.pop()
            obj = Destructible()
            game_state[pos[0]][pos[1]].append(obj)
            obj.position = pos

        starting_positions = [
            (0, 0),
            (0, width - 1),
            (height - 1, 0),
            (height - 1, width - 1)
        ]

        for crit_position in starting_positions:
            for i in range(-1, 2):
                row = crit_position[0] + i
                if (row < 0) or (row >= height):
                    continue
                for j in range(-1, 2):
                    col = crit_position[1] + j
                    if (col < 0) or (col >= width):
                        continue
                    if get_destructible_at(row, col, game_state):
                        game_state[row][col] = []

        random.shuffle(starting_positions)
        for i, player in enumerate(self.players):
            player.position = starting_positions[i]
            game_state[starting_positions[i][0]][starting_positions[i][1]].append(player)
            print(f'Player {player} got starting position {starting_positions[i]}')

        return game_state

    def iter_game_objects(self):
        for row in range(len(self.game_state)):
            for col in range(len(self.game_state[row])):
                obj = self.game_state[row][col]
                if obj:
                    yield from iter(obj)

    def update_game_state(self):
        delta = time.time() - self._last_update
        self._last_update = time.time()
        if self.finished:
            return

        self.timer -= delta

        self.update_bombs_clocks(delta)
        for bomb in self.bombs:
            if bomb.due_to_explode():
                self.explode_single_bomb(bomb)

        self.update_fires_clocks(delta)
        for fire in self.fires:
            if fire.ttl <= 0:
                self.remove_from_slot(fire.position, fire)
                self.fires.remove(fire)

        for fire in self.fires:
            players = self.check_fire_hits_players(fire)
            if players:
                for pl in players:
                    if fire.hits(pl):
                        self.kill_player(pl)
            for bomb in self.bombs:
                if fire.hits(bomb):
                    self.explode_single_bomb(bomb)

        for player in self.players:
            player.stats.record_bomb_count()
            powerup = self.get_powerup(player)
            if not powerup:
                continue
            powerup.apply(player)
            player.stats.incr_powerup_pickup(powerup.power_up_id)
            self.remove_from_slot(powerup.position, powerup)

        try:
            data = self.remote_queue.get(block=False)
            player, ev = self.queue_event_to_pygame_compatible(data)
            self.handle_player_event(player, ev)
        except queue.Empty:
            pass

        for player, ev_player_type in zip(self.players, ALL_PLAYER_EVENT_TYPES, ):
            for ev in pygame.event.get(eventtype=ev_player_type):
                self.handle_player_event(player, ev)

        if self.timer < 0:
            self.finished = True
            for player in self.players:
                player.kill()

        # draw
        if all(p.is_dead() for p in self.players):
            self.finished = True
            self.winner = None
        else:
            # at least one is not dead
            alive = self.players[:]
            for player in self.players:
                if player.is_dead():
                    alive.remove(player)
            if len(alive) == 1:
                self.finished = alive[0]
                self.winner = alive[0]

    def get_powerup(self, player: Player) -> BasePowerUp:
        slot = self.game_state[player.position[0]][player.position[1]]
        for thing in slot:
            if isinstance(thing, BasePowerUp):
                return thing

    def handle_player_event(self, player: Player, ev: pygame.event.Event) -> None:
        if self.finished:
            return

        if ev.action == 'move':
            if not player.can_move():
                return
            if self.move_player(player, ev.direction):
                player.reset_action_timer()

        if ev.action == 'bomb':
            self.spawn_player_bomb(player)

    def move_player(self, player: Player, direction) -> bool:
        """Returns whether the player had a valid movement"""
        if player.is_movement_disabled():
            return False

        next_pos = {
            'left': (player.position[0], player.position[1] - 1),
            'right': (player.position[0], player.position[1] + 1),
            'down': (player.position[0] + 1, player.position[1]),
            'up': (player.position[0] - 1, player.position[1])
        }[direction]

        if self.is_valid(next_pos):
            self.remove_from_slot(player.position, player)
            self.add_to_slot(next_pos, player)
            player.position = next_pos
            return True

        return False

    def position_is_out_of_bounds(self, position):
        if position[0] < 0 or position[0] >= len(self.game_state):
            return True
        if position[1] < 0 or position[1] >= len(self.game_state[0]):
            return True
        return False

    def is_valid(self, position):
        if self.position_is_out_of_bounds(position):
            return False
        if not player_can_move_into(self.game_state, position):
            return False
        return True

    def remove_from_slot(self, position, value):
        self.game_state[position[0]][position[1]].remove(value)

    def add_to_slot(self, position, value):
        self.game_state[position[0]][position[1]].append(value)

    def spawn_player_bomb(self, player: Player):
        if not player.has_bombs_left():
            return

        obj = Bomb(player)
        obj.position = (player.position[0], player.position[1])
        self.game_state[player.position[0]][player.position[1]].append(obj)
        self.bombs.append(obj)

        player.current_bombs += 1
        player.stats.incr_bombs_placed()

    def get_state_as_json(self, as_player_index=None):
        current_player = self.players[as_player_index]
        objs = []
        for obj in self.iter_game_objects():
            if obj == current_player:
                objs.append(obj.as_json(is_me=True))
            else:
                objs.append(obj.as_json())
        return objs

    def queue_event_to_pygame_compatible(self, data):
        player_index = data['player']
        del data['player']
        player = {
            1: EVENT_PLAYER_1,
            2: EVENT_PLAYER_2,
            3: EVENT_PLAYER_3,
            4: EVENT_PLAYER_4,
        }[player_index]
        return self.players[player_index - 1], pygame.event.Event(player, **data)

    def explode_single_bomb(self, bomb: Bomb):
        expl_range = bomb.explosion_range
        position = bomb.position
        self.remove_from_slot(position, bomb)
        self.bombs.remove(bomb)
        bomb.owner.current_bombs -= 1

        self.spawn_fire_at(position)
        for direction in ('up', 'down', 'left', 'right'):
            for i in range(1, expl_range + 1):
                cell = get_cell_in_direction(position, direction, i)
                if self.position_is_out_of_bounds(cell):
                    break
                if slot_is_indestructible(cell[0], cell[1], self.game_state):
                    break
                if get_destructible_at(cell[0], cell[1], self.game_state):
                    self.destroy_destructible_at(cell, destroyed_by=bomb.owner)
                    self.spawn_fire_at(cell)
                    break
                self.spawn_fire_at(cell)

    def destroy_destructible_at(self, position, destroyed_by: Player):
        for item in self.game_state[position[0]][position[1]]:
            if isinstance(item, Destructible):
                self.remove_from_slot(position, item)
                destroyed_by.stats.destructible_destroyed(item)
                if random.random() < self.get_powerup_chance():
                    # spawn random powerup
                    powerup = random.choice(self.POWERUP_CLASSES)()
                    powerup.position = position
                    self.add_to_slot(position, powerup)

    def update_bombs_clocks(self, delta: float) -> None:
        for bomb in self.bombs:
            bomb.time_to_explosion -= delta

    def spawn_fire_at(self, cell):
        fire = Fire()
        self.add_to_slot(cell, fire)
        fire.position = cell
        self.fires.append(fire)

    def update_fires_clocks(self, delta: float):
        for fire in self.fires:
            fire.ttl -= delta

    def check_fire_hits_players(self, fire: Fire) -> List[Player]:
        players = []
        for player in self.players:
            if (fire.position[0], fire.position[1]) == (player.position[0], player.position[1]):
                players.append(player)
        return players

    def kill_player(self, player: Player):
        if player.is_dead():
            return
        print(f'Killing {player}')
        player.kill()

    def get_powerup_chance(self):
        return 0.33
