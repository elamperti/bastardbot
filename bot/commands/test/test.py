from bot.ICommandPlugin import ICommandPlugin

class CommandTest(ICommandPlugin):
	aliases = ['test']

	def execute(self, callback, *args, **kwargs):
		callback(kwargs.get('conversation_id'), "test is ok")