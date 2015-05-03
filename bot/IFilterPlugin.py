#!/usr/bin/env python
# coding=utf-8

from yapsy.IPlugin import IPlugin

class IFilterPlugin(IPlugin):
	# Not implemented yet
	def activate(self):
		pass

	# Not implemented yet
	def deactivate(self):
		pass

	def apply(self, *args, **kwargs):
		pass