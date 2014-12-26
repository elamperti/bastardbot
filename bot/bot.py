#!/usr/bin/env python
# coding=utf-8
import os
import signal
import sys
import time
import logging
# FIXME: workaround for hangups path
# Not needed anymore.
#sys.path.insert(0, os.getcwd() + '/hangups') 
import asyncio
import hangups
from hangups.ui.utils import get_conv_name


class BotMain(object):
    def __init__(self, cookies_path = 'bot/cookies', max_retries = 1):
        """ Init function """
        self.__cookies_path = cookies_path
        self.__max_retries = max_retries
        self.__client = None
        self.__user_list = None
        self.__conversation_list = None
        self.__log = logging.getLogger('bastardbot')
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

    def __on_connect(self, initial_data):
        """ Handle connection """
        self.__log.debug("Bot connected")
        
        self.__user_list = hangups.UserList(self.__client, 
                                            initial_data.self_entity,
                                            initial_data.entities,
                                            initial_data.conversation_participants)
        
        self.__conversation_list = hangups.ConversationList(self.__client,
                                                            initial_data.conversation_states,
                                                            self.__user_list,
                                                            initial_data.sync_timestamp)
        
        self.__conversation_list.on_event.add_observer(self.__on_conversation_event)

        self.__log.debug('Initial conversations:')
        for c in self.__conversation_list.get_all():
            self.__log.debug('  {} ({})'
                             .format(get_conv_name(c, truncate=True), c.id_))

    def __on_disconnect(self):
        """ Handle disconnect """
        # derp, we were kicked out by the network
        self.__log.warning("Bot was kicked out by the network")

    def __on_conversation_event(self, event):
        """ Handle conversation events """
        if isinstance(event, hangups.ChatMessageEvent):
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
                    loop.run_until_complete(self.__client.connect())
                    sys.exit(0)
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
        asyncio.async(
            self.__client.disconnect()
        ).add_done_callback(lambda future: future.result())
