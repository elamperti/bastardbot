#!/usr/bin/env python
# coding=utf

from models import *

class BotBrain(object):
    def __init__(self):
        botdb.connect()
        #botdb.drop_tables([User, Conversation, Message], safe=True)
        botdb.create_tables([User, Conversation, Message], safe=True)
        self.__commands = ['echo', 'test', 'alias', 'config']

    def register_user(self, full_name, gaia_id, alias=None):
        if not alias:
            alias = gaia_id
        try:
            User.create(display_name=full_name, alias=alias, gaia_id=gaia_id)
        except ModelException.IntegrityError:
            pass

    def register_conversation(self, conv_name, conv_id):
        try:
            Conversation.create(name=conv_name, conv_id=conv_id)
        except ModelException.IntegrityError:
            pass

    def parse_message(self, conversation_id, author, message, timestamp, callback):
        #print("[{}]{}: {} [{}]"
        #      .format(conversation_id, author, message, timestamp))

        ########### DEBUG -z
        db_conv = Conversation.get(Conversation.conv_id == conversation_id)
        db_author = User.get(User.gaia_id == author)

        Message.create(content=message, conversation=db_conv, author=db_author, message_type=1, date_created=timestamp)
        ########### /DEBUG -z

        if message.startswith("/"):
            command = message.split(" ", 1)[0].strip("/")
            message = message.replace("/%s" % command, "").strip()
            if command in self.__commands:
                getattr(self, "handle_cmd_%s" % command)(conversation_id, author, 
                                                         message, timestamp, callback)

    def handle_cmd_echo(self, conversation_id, author, message, timestamp, callback):
        callback(conversation_id, message.replace('/echo ', ''))

    def handle_cmd_test(self, conversation_id, author, message, timestamp, callback):
        callback(conversation_id, "test is ok")

    def handle_cmd_alias(self, conversation_id, author, message, timestamp, callback):
        try:
            user = User.get(User.gaia_id == author)
            cmdargs = message.split(" ")[1::]
            if len(cmdargs) == 1 and cmdargs[0]:
                cmdargs = cmdargs.pop()
                user.alias = cmdargs
                user.save()
                callback(conversation_id, "alias set to %s" % cmdargs)
            else:
                callback(conversation_id, "your alias is %s" % user.alias)    
        except:
            callback(conversation_id, "user not registered")

    def handle_cmd_config(self, conversation_id, author, message, timestamp, callback):
        if message.find(" ") != -1:
            key, value = message.split(" ", 1)
            if key == "private":
                db_conv = Conversation.get(Conversation.conv_id == conversation_id)
                db_conv.private = (value.lower().strip() == "true")
                db_conv.save()
                if db_conv.private:
                    callback(conversation_id, "conversation set as private")
                else:
                    callback(conversation_id, "conversation set as public")
        else:
            callback(conversation_id, "invalid config key")
