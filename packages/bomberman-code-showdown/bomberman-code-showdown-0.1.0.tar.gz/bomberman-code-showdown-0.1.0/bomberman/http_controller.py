import asyncio
import json
import threading

from aiohttp import web
from aiohttp.web_runner import AppRunner


class HttpController:
    def __init__(self, host, port, game):
        self.host, self.port = host, port
        self.game = game

    def start_server(self):
        app = self.create_app()
        thread = threading.Thread(target=self._server, args=(app,))
        thread.start()

    def create_app(self):
        app = web.Application()
        app.add_routes([
            web.post('/player-{player_index}/action', self.handle_player_movement),
            web.get('/player-{player_index}/game-state', self.handle_get_game_state),
        ])
        return AppRunner(app)

    def _server(self, runner):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, self.host, self.port)
        loop.run_until_complete(site.start())
        loop.run_forever()

    def _error(self, err):
        return web.Response(body=json.dumps({'status': 'error', 'message': err}), status=400)

    async def handle_player_movement(self, request):
        player_index = int(request.match_info['player_index'])

        data = await request.json()

        if data not in [
            {"action": "bomb"},
            {"action": "move", "direction": "up"},
            {"action": "move", "direction": "down"},
            {"action": "move", "direction": "left"},
            {"action": "move", "direction": "right"},
        ]:
            return self._error("Unrecognized event")

        self.game.remote_queue.put({'player': player_index, **data})

        return web.Response(body=json.dumps({
            'player': player_index,
            'status': 'ok'
        }))

    async def handle_get_game_state(self, request):
        player_index = int(request.match_info['player_index']) - 1
        return web.Response(body=json.dumps({
            'objects': self.game.get_state_as_json(as_player_index=player_index),
            'player': self.game.players[player_index].get_complete_json()
        }))
