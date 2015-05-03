#!/usr/bin/env python
# coding=utf-8

from yapsy.PluginManager import PluginManager
# Plugin categories
from bot.ICommandPlugin import ICommandPlugin
from bot.IFilterPlugin import IFilterPlugin

from models import *

class BotBrain(object):
    def __init__(self):
        botdb.connect()

        #botdb.drop_tables([User, Conversation, Message], safe=True)
        botdb.create_tables([User, Conversation, Message], safe=True)

        # Init plugins
        print ("Looking for plugins...")
        self._plugins = PluginManager(categories_filter={
            "Command" : ICommandPlugin,
            "Filter"  : IFilterPlugin
        })
        self._plugins.setPluginPlaces(['bot/commands/', 'bot/filters/'])
        self._plugins.collectPlugins()

        # Load slash commands
        self.__commands = {}
        print ("╠ Commands")
        for plugin in self._plugins.getPluginsOfCategory("Command"):
            print ("║  * Found «%s»" % plugin.name)
            for cmdname in plugin.plugin_object.aliases:
                self.__commands[cmdname] = plugin.plugin_object.execute
                # print ("using slash command '%s'" % cmdname)

        # Load filters
        print ("╚ Filters")
        self.filters = self._plugins.getPluginsOfCategory("Filter")
        for plugin in self.filters:
            print ("   * Found «%s»" % plugin.name)

        print ("Done.\n")

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

        context = {
            'conversation_id': conversation_id,
            'author'   : author,
            'message'  : message,
            'timestamp': timestamp,
            'callback' : callback
        }

        if message.startswith("/"):
            command, context['message'] = message.split(" ", 1)
            command = command.strip("/")

            if command in self.__commands:
                context['command'] = command
                self.__commands[command](context.pop('callback'), **context)

        else: # Filter it!
            for filter in self.filters:
                filter.plugin_object.apply(**context)

    # FIXME: create a plugin to replicate this
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
