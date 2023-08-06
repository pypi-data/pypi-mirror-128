from .commands import (chat, kick, leaveRoom, startRoom, switchBracket,
                       switchBracketHost, transferOwnership, updateConfig, clearChat, unban)
from .urls import room


class Room:
    def __init__(self, data, bot):
        self.id = data['id']
        self.opts = data['game']['options']
        self.meta = data['meta']
        self.name = self.meta['name']
        self.state = data['game']['state']
        self.match = data['game']['match']
        self.type = data['type']
        self.owner = data['owner']
        self.players = data['players']
        self.invite = room + self.id
        self.bot = bot
        self.bracket = self.getPlayer(bot.id)['bracket']
        self.inGame = self.state == 'ingame'
        self.playing = self.bracket == 'player'
        self.game = None
        self.left = False

    async def switchBracket(self, playing: bool, uid=None):
        bracket = ['spectator', 'player'][playing]
        self.bracket = bracket
        bot = self.bot
        if uid:
            await self.bot.connection.send(switchBracketHost(bot.messageId, bracket, uid))
        else:
            await self.bot.connection.send(switchBracket(bot.messageId, bracket))

    async def leave(self):
        bot = self.bot
        await self.bot.connection.send(leaveRoom(bot.messageId))
        self.left = True

    def getPlayer(self, id):
        return self.players[index] if (index := self._getIndex(id)) is not None else None

    def _getIndex(self, id):
        players = self.players
        for i, player in enumerate(players):
            if player['_id'] == id:
                return i
        return None

    async def makeOwner(self, uid):
        await self.bot.connection.send(transferOwnership(self.bot.messageId, uid))

    async def kickUser(self, uid, duration=900):
        await self.banUser(uid, duration)

    async def banUser(self, uid, duration=2592000):
        await self.bot.connection.send(kick(self.bot.messageId, uid, duration))

    async def unbanUser(self, name):
        name = name.lower()
        await self.bot.connection.send(unban(self.bot.messageId, name))

    async def startGame(self):
        await self.bot.connection.send(startRoom(self.bot.messageId))

    async def send(self, message):
        await self.bot.connection.send(chat(str(message), self.bot.messageId))

    async def updateConfig(self, data):
        _data = []
        for name, value in data.items():
            _data.append({'index': name, 'value': value})
        await self.bot.connection.send(updateConfig(self.bot.messageId, _data))

    async def clearChat(self):
        await self.bot.connection.send(clearChat)

    def getBots(self):
        res = []
        for u in self.players:
            if u['bot']:
                res.append(u)
        return res

    def getAnons(self):
        res = []
        for u in self.players:
            if u['anon']:
                res.append(u)
        return res

    def getSpectators(self):
        res = []
        for u in self.players:
            if u['bracket'] == 'spectator':
                res.append(u)
        return res

    def getPlaying(self):
        res = []
        for u in self.players:
            if u['bracket'] == 'player':
                res.append(u)
        return res
