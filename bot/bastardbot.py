import os
import sys
import logging
# FIXME: workaround for hangups path
sys.path.insert(0, os.getcwd() + '/hangups')

from tornado import ioloop
import hangups

from .hangupsadapters import ChatMessage

class BastardBot(object):
    def __init__(self):
        super(BastardBot, self).__init__()
        self.__log = logging.getLogger('BastardBot')
        self.__database = None
        self.__users = None
        self.__conversations = None

    ########################################
    # LAUNCH RELATED 
    ########################################
    def start(self):
        # auth cookie
        try:
            cookies = hangups.auth.get_auth_stdin('cookies')
        except auth.GoogleAuthError as e:
            self.__log.critical('Authentication error %s', e)
            raise e
       
        # init client
        self.__client = hangups.client.Client(cookies)

        # hooks
        self.__client.on_connect.add_observer(self.__on_connect)
        self.__client.on_disconnect.add_observer(self.__on_disconnect)

        # launching the tornado
        try:
            ioloop.IOLoop.instance().run_sync(self.__client.connect)
        except ioloop.TimeoutError:
            pass

    def stop(self):
        ioloop.IOLoop.instance().stop()


    ########################################
    # PUBLIC CONFIGURATION METHODS
    ########################################
    def set_database(self, database):
        self.__database = database


    ########################################
    # BOT INTERACTION FROM OUTER WORLD - TBD
    ########################################
    #def say_hello(self, name):
    #    self.output('Hello, {}! I am BotWrapper'.format(name))
    #
    #def send_message(self, conversation, message):
    #    try:
    #        cv = self.__conversations.get(conversation)
    #        cv.send_message(message)
    #        self.output('To {}: {}'.format(conversation, message))
    #    except:
    #        self.output('ERROR SENDING MESSAGE')


    ########################################
    # PRIVATE METHODS
    ########################################
    def __parse_recent_messages(self):
        # FIXME ToDo
        pass

    def __parse_message(self, chatmessage):
        self.__log.debug("%s - %s", chatmessage.conv_id(), chatmessage.text())
        self.__save_message(chatmessage)

    def __save_message(self, chatmessage):
        # FIXME operations are too tied
        # FIXME try catch
        author = chatmessage.author()
        #self.__add_author(chatmessage.author())
        self.__database.put_message(
            chatmessage.conv_id(),
            chatmessage.text(),
            None, #author.gaia_id, # INTS ARE TO BIG
            chatmessage.timestamp()
        )
        self.__database._commit() # FIXME John

    def __sync_conversations(self):
        conversations = [c['conv_id'] for c in self.__database.get_conversations()]
        for conv in self.__conversations.get_all():
            if conv._id not in conversations:
                self.__database.put_conversation(
                    conv.id_,
                    conv.name,
                    None # FIXME fill with users
                )
        self.__database._commit() # FIXME John
        self.__log.debug("Conversations synced")

    def __add_author(self, author):
        self.__database.put_author(int(author.gaia_id), "None")
        self.__database._commit() # FIXME John
        self.__log.debug("Author added: %s", author.gaia_id)

    #FIXME: disabling this for now
        #print("Loading initial conversations")
        #for conversation in self.__conversations.get_all():
        #    self.__add_conversation(conversation)
        #    for message in conversation.chat_messages:
        #        self.__add_message(message)
        #print("Conversations loaded!") 


    ########################################
    # EVENTS HANDLERS
    ########################################
    def __on_connect(self, initial_data):
        """Handle connecting for the first time."""
        
        self.__log.info("Bot is connected")

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
        self.__sync_conversations()

        self.__conversations.on_message.add_observer(self.__on_message)

    def __on_disconnect(self):
        """Handle disconnecting."""
        # derp, we were kicked out by the network
        self.__log.warn("Bot was kicked out by the network")

    def __on_message(self, message):
        if message.user_id.gaia_id != self.__id:
            self.__log.debug("Bot has received a message!")
            try:
                conversation = self.__conversations.get(message.conv_id)
                self.__parse_message(ChatMessage(conversation, message))
            except KeyError:
                self.__log.warn("New conversation detected! [%s]", message.conv_id)
            