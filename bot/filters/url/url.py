import re

from bot.IFilterPlugin import IFilterPlugin

from models import User, Conversation, Message

class FilterURL(IFilterPlugin):
    def __init__(self):
        self._url_pattern = re.compile(r"\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", re.IGNORECASE)

    def apply(self, *args, **kwargs):       
        db_conv = Conversation.get(Conversation.conv_id == kwargs.get('conversation_id'))
        db_author = User.get(User.gaia_id == kwargs.get('author'))
        timestamp = kwargs.get('timestamp')

        url_matches = self._url_pattern.match(kwargs.get('message'))
        if url_matches:
            urls = url_matches.groups()
            for url in urls:
                if url:
                    Message.create(content=url, conversation=db_conv, author=db_author, message_type=2, date_created=timestamp)
