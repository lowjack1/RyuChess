import os
import traceback

import tornado.ioloop
import tornado.web

import RyuChess.handlers as handlers
import RyuChess.settings as settings


class Application(tornado.web.Application):
    def __init__(self, config, port):
        routes = [
            (r"/", handlers.common.HomePage),
            (r"/homepage", handlers.common.HomePage),
            (r"/signup", handlers.common.Signup),
            (r"/login", handlers.common.Login),
            (r"/about", handlers.common.About),
            (r"/play_game", handlers.common.PlayGame),
            (r"/api/generic", handlers.common.GenericApi)
        ]
        super(Application, self).__init__(handlers=routes, **config)
        # For the world to exist peacefully, this application should always listen on localhost.
        http_server = self.listen(port, address='127.0.0.1')
        # Set "xheaders" as true. Currently we are using this so that the over-write behaviour on "remote_ip" can be done
        # using the request headers present "X-Real-Ip" / "X-Forwarded-For". This is important as in our architecture Tornado sits behind a proxy server
        http_server.xheaders = True