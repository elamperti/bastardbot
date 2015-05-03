import cherrypy

from webserver.controllers.basecontroller import BaseController
from webserver.template import template

from models import Conversation, User, Message

class BastardController(BaseController):
    @cherrypy.expose
    def default(self, *args, **kwargs):
        return "404 Not Found"

    @cherrypy.expose
    @template("home")
    def index(self, *args, **kwargs):
        return {}

    @cherrypy.expose
    def logout(self):
        cherrypy.lib.sessions.expire()
        self.redirect('/')

    @cherrypy.expose
    @template("links")
    def links(self, page=1):
        messages = Message.select().where(Message.message_type == 2)
        return {'messages': messages}

    @cherrypy.expose
    @template("log")
    def log(self, conv_id=0):
        if conv_id is 0:
            self.redirect('/conversations')
        else:
            try:
                conversation = Conversation.get(Conversation.conv_id == conv_id)
            except:
                # cherrypy.request.session.alerts.warn("Conversation ID not found")
                self.redirect('/conversations')

            # Now we know there is a conversation with that ID, check for messages
            try:
                messages = Message.select().where(Message.conversation == conversation and Message.message_type == 1)
                print (messages)
                return {'conversation': conversation, 'messages': messages}
            except:
                return {'conversation': conversation, 'no_messages': 1}

    @cherrypy.expose
    @template("conversations")
    def conversations(self, conv_id=0):
        if conv_id is not 0:
            self.redirect('/log/' + conv_id)
        conversations = Conversation.select().where(Conversation.private == False)
        return {'conversations': conversations}

    @cherrypy.expose
    @template("users")
    def users(self):
        users = User.select()
        return {'users': users}