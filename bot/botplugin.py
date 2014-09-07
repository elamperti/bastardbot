from cherrypy.process import plugins
from .botwrapper import BotWrapper

class BotPlugin(plugins.SimplePlugin):
    def __init__(self, bus):
        """Initialization"""
        super(BotPlugin, self).__init__(bus)
        self.bot = BotWrapper(self.bus.log)
        
    def start(self):
        self.bus.log('Starting up BotPlugin')
        self.bus.subscribe("bot-sayhello", self.say_hello)
        self.bus.subscribe("bot-sendmsg", self.send_message)
        self.bot.start()
        
    def stop(self):
        self.bot.stop()
        self.bus.log('Stopping down BotPlugin')
        self.bus.unsubscribe("bot-sayhello", self.say_hello)
        self.bus.unsubscribe("bot-sendmsg", self.send_message)

    def say_hello(self, name):
        self.bot.say_hello(name)

    def send_message(self, conversation, message):
        self.bot.send_message(conversation, message)