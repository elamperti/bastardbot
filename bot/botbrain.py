#!/usr/bin/env python
# coding=utf
import peewee
from models import *

class BotBrain(object):
    def __init__(self):
        botdb.connect()
        botdb.drop_tables([User, Conversation], safe=True) # change to true after debug
        botdb.create_tables([User, Conversation])
        self.__commands = ['echo', 'test', 'alias']

    def register_user(self, full_name, gaia_id, alias=None):
        if not alias:
            alias = gaia_id
        User.create(display_name=full_name, alias=alias, gaia_id=gaia_id)

    def register_conversation(self, conv_name, conv_id):
        Conversation.create(name=conv_name, conv_id=conv_id)

    def parse_message(self, conversation_id, author, message, timestamp, callback):
        print("[{}]{}: {} [{}]"
              .format(conversation_id, author, message, timestamp))
        if message.startswith("/"):
            command = message.split(" ", 1)[0].strip("/")
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
