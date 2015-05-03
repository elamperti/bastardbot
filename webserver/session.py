#!/usr/bin/python

import cherrypy

from webserver.alerts import Alerts


class Session():

    def __init__(self, CPSession):
        self._session = CPSession
        self.alerts = Alerts(CPSession)
        self.id = CPSession.id

    def __del__(self):
        cherrypy.request.session.save()

    def get(self, *args, **kwargs):
        return self._session.get(*args, **kwargs)

    def regenerate(self):
        self._session.clear()
        self._session.regenerate()
        self.id = self._session.id

    def set(self, params):
        for key, value in params.iteritems():
            self._session[key] = value

    def unset(self, key):
        self._session[key] = None

    def isLoggedIn(self):
        user = self._session.get('user')

        # This is certainly not pythonic.
        if user:
            return True
        else:  # user is not defined!
            return False

    @staticmethod
    def restricted(f):
        def _checkUser(*args, **kwargs):
            if cherrypy.request.session.isLoggedIn():
                return f(*args, **kwargs)
            else:
                cherrypy.request.session.alerts.error("You are not logged in.")
                cherrypy.request.session.set({
                    'origin': cherrypy.lib.httputil.urljoin(
                        cherrypy.request.script_name,
                        cherrypy.request.path_info
                    )
                })
                raise cherrypy.HTTPRedirect("/")

        return _checkUser

    @staticmethod
    def handler():
        try:
            foo = Session(cherrypy.session)
            cherrypy.request.session = foo
        except:
            pass
