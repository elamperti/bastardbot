# -*- coding: utf-8 -*-
import cherrypy

class BaseController(object):

    @classmethod
    def redirect(cls, dest):
        raise cherrypy.HTTPRedirect(dest)

    @classmethod
    def request(cls):
        return cherrypy.request

    @classmethod
    def error(cls, code=500, message=""):
        raise cherrypy.HTTPError(code, message)

    @classmethod
    def notFound(cls, *args, **kwargs):
        cls.error(404, "Page not found")
