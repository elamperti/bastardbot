from hangups import auth
from hangups import client
import hangups
from tornado import ioloop

from time import sleep
from database import BastardSQL

class BastardBot():
    def __init__(self, database):
        self.__db = database
        # auth cookie
        try:
            cookies = auth.get_auth_stdin('cookies')
        except auth.GoogleAuthError as e:
            print('Login failed ({})'.format(e))
            sys.exit(-1)

        # init client
        self.__client = client.Client(cookies)

        # hooks
        self.__client.on_connect.add_observer(self.__on_connect)
        self.__client.on_disconnect.add_observer(self.__on_disconnect)
        self.__client.on_message.add_observer(self.__on_message)

        # generic hook for debugging
        self.__client.on_typing.add_observer(self.__on_generic_event)
        self.__client.on_conversation.add_observer(self.__on_generic_event)

    def sync(self):
        try:
            ioloop.IOLoop.instance().run_sync(self.__client.connect)
        except ioloop.TimeoutError:
            pass

    def __add_conversation(self, conversation):
        """Adds a conversation (if not exists)"""
        #FIXME Otimize the hell of this
        if not self.__db.get_conversation((conversation.id_,)).fetchone():
            self.__db.put_conversation(
                conversation.id_, 
                conversation.name, 
                ";-;".join([u.full_name for u in conversation.users])
            )
            self.__db.commit()

    def __add_message(self, message):
        """Adds a message in a specific conversation"""
        #FIXME Otimize the hell of this
        if self.__db.get_conversation((message.conv_id,)).fetchone():
            self.__db.put_message(
                message.conv_id, 
                message.text, 
                message.user_id.gaia_id, 
                message.timestamp
            )
            self.__db.commit()


    def __on_connect(self):
        """Handle connecting for the first time."""
        print ("Connected!")
        self.__id = self.__client.self_user_id.gaia_id
        self.__conversations = hangups.ConversationList(self.__client);
        self.__users = hangups.UserList(self.__client)

        print("Loading initial conversations")
        for conversation in self.__conversations.get_all():
            self.__add_conversation(conversation)
            for message in conversation.chat_messages:
                self.__add_message(message)
            

        #print("Debug!")
        #r = self.__client.searchentities("christian", 5)
        #r.add_done_callback(self.__on_results)

        #self.conv_list = hangups.ConversationList(self.__client)
        #self.user_list = hangups.UserList(self.__client)
        #print(self.conv_list)
        #print(self.user_list)
        
        #for conver in self.conv_list.get_all():
        #    for message in conver.chat_messages:
        #        try:
        #            user = conver.get_user(message.user_id).full_name
        #        except:
        #            user = "User left"
        #        time = message.timestamp
        #        text = message.text
        #        #print("[{} - {}] {}".format(user, time, text))
        #        print(message.user_id)

        #print('CONVERSATIONS {}'.format(len(self.__client.initial_conversations)))
        #convlist = list(self.__client.initial_conversations)
        #for conv in convlist:
        #    one = self.__client.initial_conversations[conv]
        #    for c in one.chat_messages:
        #        print(c)
    
    def __on_disconnect(self):
        """Handle disconnecting."""
        print('Connection lost')

    def __on_generic_event(self, args):
        #print("event")
        #print(args)            
        pass

    def __on_results(self, futureobj):
        try:
            print(futureobj.result())
        except:
            print('did not work')

    def __on_message(self, message):
        if message.user_id.gaia_id != self.__id:
            print("Message received from {}: {}".format(message.user_id, message.text))
            self.__add_message(message)


if __name__ == '__main__':
    print("Initializing the BastardBot database...")
    botdb = BastardSQL()
    print("DATABASE RESET ENABLED - FIX ME")
    botdb._populate()
    print("Initializing the BastardBot client...")
    bot = BastardBot(botdb)
    try:
        print("Main loop started")
        while(True):
            bot.sync()
            sleep(2)
            print("Looped")
    except KeyboardInterrupt:
        print("Keyboard interrupt!")