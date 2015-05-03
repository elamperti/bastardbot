#!/usr/bin/env python
# coding=utf-8

from yapsy.IPlugin import IPlugin

class ICommandPlugin(IPlugin):
	aliases = []

	# Not implemented yet
	def activate(self):
		pass

	# Not implemented yet
	def deactivate(self):
		pass

	def execute(self, callback, *args, **kwargs):
		pass
