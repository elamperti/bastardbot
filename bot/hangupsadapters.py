class ChatMessage(object):
    def __init__(self, conversation, chat_message):
        self.__conversation = conversation
        self.__chat_message = chat_message

    def conv_id(self):
        return self.__conversation.id_

    def author(self):
        return self.__chat_message.user_id

    def text(self):
        return self.__chat_message.text

    def timestamp(self):
        return self.__chat_message.timestamp

    def reply(self, text):
        self.__conversation.send_message(text)