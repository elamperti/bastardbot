class MessageFilters(object):
    def __init__(self):
        self.__filters = []

    def add_filter(self, filter, priority = None):
        if priority:
            self.__filters.insert(priority, filter)
        else:
            self.__filters.append(filter)

    def parse_message(self, chatmessage):
        # FIXME parse all for now
        if self.__filters:
            [mfilter.parse(chatmessage) for mfilter in self.__filters]

class Filter(object):
    def __init__(self):
        self._result = None

    def parse(self, chatmessage):
        raise NotImplemented

class PlainFilter(Filter):
    def __init__(self, database):
        super(PlainFilter, self).__init__()
        self.__database = database

    def parse(self, chatmessage):
        self.__database.put_message(
            chatmessage.conv_id(),
            chatmessage.text(),
            None, #author.gaia_id, # INTS ARE TO BIG
            chatmessage.timestamp()
        )
        self.__database._commit() # FIXME John
        return True

class EchoCommand(Filter):
    def parse(self, chatmessage):
        text = chatmessage.text()
        if text.find('/echo ') == 0:
            chatmessage.reply(text.replace('/echo ', ''))