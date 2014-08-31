import cherrypy
from controllers.basecontroller import BaseController

class DefaultController(BaseController):
    @cherrypy.expose
    def index(self, *args, **kwargs):
        return "Hi"