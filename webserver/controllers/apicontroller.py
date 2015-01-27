import cherrypy

from controllers.basecontroller import BaseController


class APIController(BaseController):
    def __init__(self):
        pass

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return "Unknown method"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def list(self, *args, **kwargs):        
        res = cherrypy.thread_data.db.get_conversations()
        conversations = []
        for item in res:
            conversations.append(cherrypy.thread_data.db.dict_factory(item))

        return conversations

    @cherrypy.expose
    def conversation(self, conv_id):
        if conv_id is not Null:
            return "Hello :)"
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def talk(self, conv_id, message):
        cherrypy.engine.publish('bot-sendmsg', conv_id, message)
        return [conv_id, message]