#!/usr/bin/python

import os
import datetime

import cherrypy
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import arrow

def arrow_humanize(value):
    obj = arrow.get(value)
    return obj.humanize()

def template(filename=None):  # , *args, **kwargs
    def wrap(f, *args, **kwargs):
        def wrapped_f(*args, **kwargs):
            params = f(*args, **kwargs)
            jinja = Environment(
                loader=FileSystemLoader('webserver/templates'),
                extensions=['jinja2.ext.with_']
            )
            jinja.filters['humanize'] = arrow_humanize

            if not filename:
                raise cherrypy.HTTPError(500, "Template not defined")
            else:
                filenames = [filename + '.tlp']  # ..scope royals vs local bastards

            if '__template' in params:
                if isinstance(params['__template'], basestring):
                    filenames.insert(0, params['__template'] + '.tlp')
                else:
                    # Don't use +=, we are leaving it *after* __template for precedence
                    filenames = [s + '.tlp' for s in params['__template']] + filenames

            try:
                t = jinja.select_template(filenames)
            except TemplateNotFound:
                raise cherrypy.HTTPError(404, "Template not found")

            t.globals['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            t.globals['session'] = cherrypy.session

            return t.render(**params)

        return wrapped_f

    return wrap
