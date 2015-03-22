import os

import cherrypy

from models import *
from webserver.controllers import *
from webserver.plugins.googleapiplugin import GoogleApiPlugin

cherrypy.config.update({
    'server.socket_host': '0.0.0.0',  # Make it visible from everywhere
    'server.socket_port': 8080, 
    'log.screen': True,
    'engine.autoreload.on': True
})

class BastardBot(object):
    def __init__(self):
        conf = {
            '/': {
                'tools.sessions.on': True,
                'tools.sessions.storage_type': "file",
                'tools.sessions.storage_path': "webserver/sessions",
                'tools.sessions.timeout': 60
            }
        }

        # Dispatch magic
        cherrypy.tree.mount(bastardcontroller.BastardController(), "", conf)
        cherrypy.tree.mount(apicontroller.APIController(), "/api/bastardbot/", conf)
        cherrypy.tree.mount(logincontroller.LoginController(), "/login", conf)

        # Google Oauth2 Plugin
        GoogleApiPlugin(cherrypy.engine, config='webserver/config/google-api.json').subscribe()

        cherrypy.engine.subscribe('start_thread', self.connectDB)
        # cherrypy.tools.sessionHandler = cherrypy._cptools.HandlerTool(sessionHandler)
        cherrypy.engine.signals.subscribe()
        self.start()

    def start(self):
        cherrypy.engine.start()
        cherrypy.engine.block()

    def stop(self):
        cherrypy.engine.stop()
        cherrypy.engine.exit()

    def connectDB(self, thread_index):
        cherrypy.thread_data.db = botdb
        cherrypy.thread_data.db.connect()
