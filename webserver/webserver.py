import os

import cherrypy

from models import *
from webserver.controllers import *
from webserver import session

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
                # 'tools.sessionHandler.on': True,
                # 'tools.sessions.on': True,
                # 'tools.sessions.storage_type': "file",
                # 'tools.sessions.storage_path': "webserver/sessions"
            }
        }

        # Dispatch magic
        cherrypy.tree.mount(bastardcontroller.BastardController(), "", conf)
        cherrypy.tree.mount(apicontroller.APIController(), "/api/bastardbot/", conf)

        # Hooking into cherrypy engine..
        #bot.BotPlugin(cherrypy.engine).subscribe()

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

# def sessionHandler():
#     '''Sadly, this can't be in Session because it requires cherrypy to be initialized.'''
#     cherrypy.request.session = session.Session(cherrypy.session)
