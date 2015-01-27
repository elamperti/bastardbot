import cherrypy

from controllers.basecontroller import BaseController
from template import template


class BastardController(BaseController):
    @cherrypy.expose
    @template("home")
    def index(self, *args, **kwargs):
        return {}

    @cherrypy.expose
    @template("links")
    def links(self, page=1):
        #FIXME: This method is asking for messages but the layout is parsing (undefined) links.
        res = cherrypy.thread_data.db.get_messages() #type=2
        links = []
        
        for item in res:
            links.append(cherrypy.thread_data.db.dict_factory(item))

        return {'links': links}

    @cherrypy.expose
    @template("conversations")
    def conversations(self):
        res = cherrypy.thread_data.db.get_conversations()
        conversations = []

        for item in res:
            conversations.append(cherrypy.thread_data.db.dict_factory(item))

        return {'conversations': conversations}