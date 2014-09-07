import os

import cherrypy

import bot
import database
from controllers import *

cherrypy.config.update({
    'server.socket_host': '0.0.0.0',  # Make it visible from everywhere
    #'server.socket_port': 1234, 
    'log.screen': True,
    'engine.autoreload.on': True
})


class BastardBot(object):

    def __init__(self):
        conf = {
            '/': {
                'tools.sessions.on': True,
                'tools.sessions.storage_type': "file",
                'tools.sessions.storage_path': "sessions"
            }
        }

        # Dispatch magic
        cherrypy.tree.mount(bastardcontroller.BastardController(), "", conf)
        cherrypy.tree.mount(apicontroller.APIController(), "/api/bastardbot/", conf)

        # Hooking into cherrypy engine...
        bot.BotPlugin(cherrypy.engine).subscribe()

        cherrypy.engine.subscribe('start_thread', self.connectDB)
        cherrypy.engine.signals.subscribe()
        self.start()

    def start(self):
        cherrypy.engine.start()
        cherrypy.engine.block()

    def stop(self):
        cherrypy.engine.stop()
        cherrypy.engine.exit()

    def connectDB(self, thread_index):
        cherrypy.thread_data.db = database.BastardSQL()

if __name__ == '__main__':
    B = BastardBot()
    