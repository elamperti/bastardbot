import re

from bot.IFilterPlugin import IFilterPlugin


class FilterDeskeeper(IFilterPlugin):
    def __init__(self):
        self._deskflip = re.compile(r".*︵ ┻━┻.*")

    def apply(self, *args, **kwargs):
        desk_has_been_flipped = self._deskflip.match(kwargs.get('message'))

        if desk_has_been_flipped:
            callback = kwargs.get('callback')
            callback(kwargs.get('conversation_id'), "┬─┬ノ( º _ ºノ)")

