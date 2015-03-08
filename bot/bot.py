#!/usr/bin/env python
# coding=utf-8

import os
import signal
import sys
import time
import logging
import asyncio

# FIXME: workaround for hangups path
sys.path.insert(0, os.getcwd() + '/hangups')
import hangups
from hangups.ui.utils import get_conv_name

from .botbrain import BotBrain

class BotMain(object):
    def __init__(self, cookies_path = 'bot/cookies', max_retries = 1):
        """ Init function """
        self.__cookies_path = cookies_path
        self.__max_retries = max_retries
        self.__client = None
        self.__id = None
        self.__user_list = None
        self.__conversation_list = None
        self.__log = logging.getLogger('bastardbot')
        self.__loop_task = None
        self.__brain = BotBrain()
        # asyncio handlers
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, lambda: self.stop())
        loop.add_signal_handler(signal.SIGTERM, lambda: self.stop())

    def __login(self):
        """ Gooogle login 

        returns False in case of failure """
        cookies = False
        self.__log.debug("Trying to log in with Google")
        try:
            cookies = hangups.auth.get_auth_stdin(self.__cookies_path)
            self.__log.debug("Bot logged in")
        except hangups.GoogleAuthError as e:
            self.__log.critical('Google authentication error %s', e)
        return cookies

    def __send_message(self, conversation_id, text):
        conversation = self.__conversation_list.get(conversation_id)
        asyncio.async(conversation.send_message([hangups.ChatMessageSegment(text)]))

    def __on_connect(self, initial_data):
        """ Handle connection """
        self.__log.debug("Bot connected")
        
        self.__id = initial_data.self_entity.id_.gaia_id

        self.__user_list = hangups.UserList(self.__client, 
                                            initial_data.self_entity,
                                            initial_data.entities,
                                            initial_data.conversation_participants)
        
        self.__conversation_list = hangups.ConversationList(self.__client,
                                                            initial_data.conversation_states,
                                                            self.__user_list,
                                                            initial_data.sync_timestamp)
        
        self.__conversation_list.on_event.add_observer(self.__on_conversation_event)
                
        # create known conversation
        self.__log.debug('Loading initial conversations:')
        for conversation in self.__conversation_list.get_all():
            self.__brain.register_conversation(get_conv_name(conversation, truncate=True), conversation.id_)
            self.__log.debug('  {} ({})'
                             .format(get_conv_name(conversation, truncate=True), conversation.id_))
        # create known users
        self.__log.debug('Loading initial users:')
        for user in self.__user_list.get_all():
            self.__brain.register_user(full_name=user.full_name, 
                                       gaia_id=user.id_.gaia_id)
            self.__log.debug('* {}'
                             .format(user.full_name))

    def __on_disconnect(self):
        """ Handle disconnect """
        # derp, we were kicked out by the network
        self.__log.warning("Bot was kicked out by the network")

    def __on_conversation_event(self, event):
        """ Handle conversation events """
        if isinstance(event, hangups.ChatMessageEvent):
            if event.user_id.gaia_id != self.__id:
                self.__brain.parse_message(event.conversation_id,
                                           event.user_id.gaia_id,
                                           event.text,
                                           event.timestamp,
                                           lambda conv_id, text: self.__send_message(conv_id, text))
                self.__log.debug("MESSAGE: [{}/{}]: {}"
                                 .format(self.__user_list.get_user(user_id=event.user_id).full_name, 
                                         event.conversation_id, 
                                         event.text))
        else:
            self.__log.debug(event)

    def start(self):
        """ Start the loop/bot """
        self.__log.debug("Starting the bot")
        cookies = self.__login()    
        if cookies:
            self.__client = hangups.Client(cookies)
        
            # event handlers
            self.__client.on_connect.add_observer(self.__on_connect)
            self.__client.on_disconnect.add_observer(self.__on_disconnect)

            # asyncio event loop and Hangouts connection with retry logic 
            # If we are forcefully disconnected, try connecting again
            loop = asyncio.get_event_loop()
            for retry in range(self.__max_retries):
                try:
                    self.__loop_task = asyncio.async(self.__db_polling_task(5))
                    loop.run_until_complete(asyncio.wait([
                        asyncio.async(self.__client.connect()),
                        self.__loop_task]))
                    loop.close()
                    self.__log.debug("Loop closed")
                except Exception as e:
                    self.__log.warning("Client unexpectedly disconnected:\n{}".format(e))
                    time.sleep(2)
                    self.__log.warning("Retry {}/{}".format(retry + 1, self.__max_retries))
            self.__log.warning('No more retries, good bye!')
        else:
            self.critical("Invalid cookies")
        sys.exit(1)

    def stop(self):
        """ Stop the loop/bot """
        self.__log.debug("Stopping the bot")
        self.__loop_task.cancel()
        asyncio.async(self.__client.disconnect()).add_done_callback(lambda future: future.result())

    @asyncio.coroutine
    def __db_polling_task(self, delay):
        for i in range(0, 10000):
            print("Count to 10000 (%s)..." % i)
            yield from asyncio.sleep(delay)
        print("Task ended")        