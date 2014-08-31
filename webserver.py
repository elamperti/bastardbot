import os

import cherrypy

from controllers import defaultcontroller

class BastardBot(object):
    def __init__(self):
        pass

    def index(self):
        return "Hi."

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
        cherrypy.tree.mount(defaultcontroller.DefaultController(), "", conf)  # , conf_for_this

        self.start()

    def index(self):
        return "Wrong way"

    def start(self):
        cherrypy.engine.start()

    def stop(self):
        cherrypy.engine.stop()
        cherrypy.engine.exit()


if __name__ == '__main__':
    B = BastardBot()
    