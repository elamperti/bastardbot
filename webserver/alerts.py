#!/usr/bin/python
# -*- coding: utf-8 -*-


class Alerts():

    def __init__(self, CPSession):
        if 'alerts' in CPSession:
            self.alerts = CPSession.get('alerts')
        else:
            self.alerts = []
        self.CPSession = CPSession

    # def __del__(self):
    # self.save() # Won't work because the request was already destroyed

    def __iter__(self):
        return self

    def save(self):
        # print "Called alerts.save for SID %s" % self.CPSession.id
        if self.alerts or 'alerts' in self.CPSession:
            self.CPSession['alerts'] = self.alerts

    def next(self):
        if not self.alerts:
            raise StopIteration
        return self.pop()

    def pop(self):
        a = self.alerts.pop()
        return {'type': a[0], 'message': a[1]}

    def add(self, alertType, message):
        self.alerts.append([alertType, message])
        self.save()

    def info(self, message):
        self.add('info', message)

    def error(self, message):
        self.add('danger', message)

    def warn(self, message):
        self.add('warning', message)

    def success(self, message):
        self.add('success', message)
