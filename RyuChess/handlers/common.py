import os
from datetime import datetime, timedelta
from dateutil import tz

import aiohttp
from tornado.web import HTTPError, escape
from tornado.ioloop import IOLoop

from .base import BaseHandler


class Signup(BaseHandler):
    async def get(self):
        return self.render("signup.html")


class Login(BaseHandler):
    async def get(self):
        return self.render("login.html")


class HomePage(BaseHandler):
    async def get(self):
        return self.render("homepage.html")


class About(BaseHandler):
    async def get(self):
        return self.render("about.html")


class PlayGame(BaseHandler):
    async def get(self):
        return self.render("play_game.html")


class GenericApi(BaseHandler):
    async def get(self):
        action = self.get_argument('action')
        if action == 'country_record':
            async with self.settings['pool'].acquire() as connection:
                q = "SELECT ID, name, alpha2, alpha3 FROM country ORDER BY name;"
                res = await connection.fetch(q)
            response_data = [
                {
                    'id': data['id'],
                    'name': data['name'],
                    'alpha2': data['alpha2'],
                    'alpha3': data['alpha3']
                }
                for data in res
            ]
            self.write_api_response(response_data)