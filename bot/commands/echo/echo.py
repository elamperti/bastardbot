from bot.ICommandPlugin import ICommandPlugin

class CommandEcho(ICommandPlugin):
	aliases = ['echo', 'say']

	def execute(self, callback, *args, **kwargs):
		callback(kwargs.get('conversation_id'), kwargs.get('message', '?'))