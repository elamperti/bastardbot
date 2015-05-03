from bot.ICommandPlugin import ICommandPlugin

from models import User

class CommandNickname(ICommandPlugin):
    aliases = ['nick', 'alias']

    def execute(self, callback, *args, **kwargs):
        conversation_id = kwargs.get('conversation_id')
        message = kwargs.get('message')

        try:
            user = User.get(User.gaia_id == kwargs.get('author'))
            cmdargs =  message.split(" ")
            if len(cmdargs) == 1 and cmdargs[0]:
                cmdargs = cmdargs.pop()
                user.alias = cmdargs
                user.save()
                callback(conversation_id, "Nick changed. Hi %s" % cmdargs)
            else:
                callback(conversation_id, "Your nick is %s" % user.alias)    
        except:
            callback(conversation_id, "User not registered")