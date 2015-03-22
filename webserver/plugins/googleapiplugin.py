# -*- coding: utf-8 -*-
import json
import httplib2
from cherrypy.process import plugins
from oauth2client.client import OAuth2WebServerFlow

class GoogleApiPlugin(plugins.SimplePlugin):
    def __init__(self, bus, config):
        plugins.SimplePlugin.__init__(self, bus)
        self.cfg = json.load(open(config))
        
    def start(self):
        self.bus.log('Starting Google Api plugin')
        # FIXME: Use flows per user https://developers.google.com/api-client-library/python/guide/django#Credentials
        self.flow = OAuth2WebServerFlow(client_id=self.cfg['client_id'],
                                       client_secret=self.cfg['client_secret'],
                                       scope=self.cfg['scopes'],
                                       redirect_uri=self.cfg['redirect_uri'])
        
        self.bus.subscribe("ga-oauth-redirect-url", self.getStep1)
        self.bus.subscribe("ga-oauth-code-exchange", self.getStep2)
        self.bus.subscribe("ga-profile-info", self.getProfile)
        
    def stop(self):
        self.bus.log('Stopping down Google Api plugin')
        self.bus.unsubscribe("ga-oauth-redirect-url", self.getStep1)
        self.bus.unsubscribe("ga-oauth-code-exchange", self.getStep2)
        self.bus.unsubscribe("ga-profile-info", self.getProfile)

    def getStep1(self):
        return self.flow.step1_get_authorize_url()

    def getStep2(self, code):
        return self.flow.step2_exchange(code)

    def getProfile(self, credentials):
        # TODO: add try block
        http = httplib2.Http()
        http = credentials.authorize(http)
        resp, content = http.request("https://www.googleapis.com/oauth2/v1/userinfo?alt=json")
        return json.loads(content.decode('utf-8'))
