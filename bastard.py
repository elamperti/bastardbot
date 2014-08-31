from hangups import auth
from hangups import client
from tornado import ioloop

from time import sleep


class Bastard():
    def __init__(self):
        # auth cookie
        try:
            cookies = auth.get_auth_stdin('cookies')
        except auth.GoogleAuthError as e:
            print('Login failed ({})'.format(e))
            sys.exit(1)

        # init client
        self._client = client.Client(cookies)
        # hooks
        self._client.on_connect.add_observer(self._on_connect)
        self._client.on_disconnect.add_observer(self._on_disconnect)
        self._client.on_message.add_observer(self._on_message)

        self.gaia_id = "117675644336605123143" # the original bastardbot


    def loop(self):
        try:
            ioloop.IOLoop.instance().run_sync(self._client.connect)
        except ioloop.TimeoutError:
            pass

    def _on_connect(self):
        """Handle connecting for the first time."""
        print ("Connected!")


    def _on_message(self, chat_message):
        print("Message received from {}: {}".format(chat_message.user_id, chat_message.text))
        
        if chat_message.user_id.gaia_id != self.gaia_id:
        #self._client.setfocus(conv_id)
        #try:
            self._client.sendchatmessage(chat_message.conv_id, "Bwaaarg!")
        #except:
        #    print("Error sending grunt")
        else:
            print("Received own message ({})".format(chat_message.text))

    def _on_disconnect(self):
        """Handle disconnecting."""
        print('Connection lost')

b = Bastard()
b._client.syncrecentconversations()

try:
    print("Main loop started.")
    while(True):
        b.loop()
        sleep(2)
        print("Looped")
except KeyboardInterrupt:
    print("Keyboard interrupt.")


print("Quitting.")
