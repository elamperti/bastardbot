import os
import sys
# FIXME: workaround for hangups path
sys.path.insert(0, os.getcwd() + '/hangups')

from threading import Thread

from tornado import ioloop
import hangups

# FIXME: maybe i'm doing an inception of threads but this is 
# an initial aproach to hook the bot into cherrypy process.
# I will review the whole thing in the next milestone.

class BotWrapper(Thread):
    def __init__(self, output):
        super(BotWrapper, self).__init__()
        self.output = output


    ########################################
    # THREAD RELATED 
    ########################################
    def run(self):
        self.output('BW: BotWrapper started')
        # auth cookie
        try:
            cookies = hangups.auth.get_auth_stdin('cookies')
        except auth.GoogleAuthError as e:
            self.output('BW: login failed ({})'.format(e))
            #sys.exit(-1) # FIXME: this line blows up everything?

        self.output('BW: authenticated')
        # init client
        self.__client = hangups.client.Client(cookies)

        # hooks
        self.__client.on_connect.add_observer(self.__on_connect)
        self.__client.on_disconnect.add_observer(self.__on_disconnect)

        self.output('BW: launching the tornado')
        try:
            ioloop.IOLoop.instance().run_sync(self.__client.connect)
        except ioloop.TimeoutError:
            pass

    def stop(self):
        self.output('BW: BotWrapper stopped')
        ioloop.IOLoop.instance().stop()


    ########################################
    # PUBLIC BOT API
    ########################################
    def say_hello(self, name):
        self.output('Hello, {}! I am BotWrapper'.format(name))
        cv = self.__conversations.get('UgxOPxGe8RTfgX8PZi94AaABAQ')
        cv.send_message('Testing hello....')

    def send_message(self, conversation, message):
        self.output('To {}: {}'.format(conversation, message))


    ########################################
    # EVENTS HANDLERS
    ########################################
    def __on_connect(self, initial_data):
        """Handle connecting for the first time."""
        self.output('BW: connected')

        # FIXME: temporaly workaround to grab self id
        self.__id = initial_data.self_entity.id_.gaia_id

        self.__users = hangups.UserList(
            initial_data.self_entity, 
            initial_data.entities,
            initial_data.conversation_participants
        )
        self.__conversations = hangups.ConversationList(
            self.__client,
            initial_data.conversation_states,
            self.__users
        )
        self.__conversations.on_message.add_observer(self.__on_message)

        #FIXME: disabling this for now
        #print("Loading initial conversations")
        #for conversation in self.__conversations.get_all():
        #    self.__add_conversation(conversation)
        #    for message in conversation.chat_messages:
        #        self.__add_message(message)
        #print("Conversations loaded!")   

    def __on_disconnect(self):
        """Handle disconnecting."""
        self.output('BW: derp, we were kicked out by the network')

    def __on_message(self, message):
        if message.user_id.gaia_id != self.__id:
            self.output(message.conv_id)
            self.output("BW: message received from {}: {} at {}".format(
                message.user_id, 
                message.text, 
                message.timestamp
            ))