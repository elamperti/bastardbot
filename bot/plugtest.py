#!/usr/bin/env python
# coding=utf-8

from yapsy.PluginManager import PluginManager

# Plugin categories
from IFilterPlugin import IFilterPlugin
from ICommandPlugin import ICommandPlugin

plugins = PluginManager(categories_filter={
	"Command" : ICommandPlugin,
	"Filter"  : IFilterPlugin
})

plugins.setPluginPlaces(['commands', 'filters'])

plugins.collectPlugins()

for pluginInfo in plugins.getPluginsOfCategory("Command"):
	#plugins.activatePluginByName(pluginInfo.name)
	print(pluginInfo.name)
	pluginInfo.plugin_object.activate()

# plugins.locatePlugins()
# candidates = plugins.getPluginCandidates()

# for i in candidates:
# 	print (i)

print("fin")