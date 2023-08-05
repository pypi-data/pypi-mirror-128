#!/usr/bin/python3
#
# deltat.py — Parse a time duration
#
# License unknown, based on work by virhilo and Peter on Stackoverflow
# Modified and packaged by Marcel Waldvogel
#

import re
from datetime import timedelta


VERSION = "1.1.2"


regex = re.compile(r'^((?P<weeks>[\.\d]+?)w)? *'
                   r'((?P<days>[\.\d]+?)d)? *'
                   r'((?P<hours>[\.\d]+?)h)? *'
                   r'((?P<minutes>[\.\d]+?)m)? *'
                   r'((?P<seconds>[\.\d]+?)s?)?$')


class TimeFormatError(ValueError):
    pass


def parse_time(time_str):
    """
    Parse a time string e.g. '2h 13m' or '1.5d' into a timedelta object.

    Based on Peter's answer at https://stackoverflow.com/a/51916936/2445204
    and virhilo's answer at https://stackoverflow.com/a/4628148/851699

    :param time_str: A string identifying a duration, e.g. '2h13.5m'
    :return datetime.timedelta: A datetime.timedelta object
    """
    parts = regex.match(time_str)
    if parts is None:
        raise TimeFormatError(
            "Could not parse any time information from '%s'. "
            "Examples of valid strings: "
            "'8h', '2d 8h 5m 2s', '2m4.3s'""" % time_str)
    time_params = {name: float(param)
                   for name, param in parts.groupdict().items() if param}
    return timedelta(**time_params)
