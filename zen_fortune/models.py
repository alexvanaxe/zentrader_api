from django.contrib.staticfiles import finders

import fortune


class Fortune(object):
    """
    Class model of a fortune. A fortune is a message (a cookie) just for fun.
    """
    cookie = ''

    def __init__(self, *args, **kwargs):
        result = finders.find('fortune/generic_fortunes1')
        self.cookie = "<br>".join(fortune.get_random_fortune(result).split("\n"))
