# -*- coding: utf-8 -*-
import cherrypy

from webserver.controllers.basecontroller import BaseController

class LoginController(BaseController):
    @cherrypy.expose
    def index(self):
        redirect_url = cherrypy.engine.publish("ga-oauth-redirect-url").pop()
        self.redirect(redirect_url)

    @cherrypy.expose
    def oauth2callback(self, code):
        if code:
            credentials = cherrypy.engine.publish("ga-oauth-code-exchange", code).pop()
            # 'id': 'GAIA_ID', 
            # 'given_name': 'NAME', 
            # 'family_name': 'SURNAME', 
            # 'name': 'NAME SURNAME [(NICK)]', 
            # 'locale': 'en-US', 
            # 'picture': 'photo.jpg'
            profile = cherrypy.engine.publish("ga-profile-info", credentials).pop()
            cherrypy.session['logged'] = True
            cherrypy.session['ga-oauth2'] = credentials
            cherrypy.session['gaia_id'] = profile['id']
            cherrypy.session['display_name'] = profile['given_name']
            cherrypy.session['full_name'] = profile['name']
            cherrypy.session['avatar_img'] = profile['picture']
        # TODO: add alert in case of oauth reject
        self.redirect('/')
