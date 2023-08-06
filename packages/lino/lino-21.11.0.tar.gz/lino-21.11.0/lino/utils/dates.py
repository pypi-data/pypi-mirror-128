# Copyright 2014-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Defines classes related to date ranges.
"""

import collections
from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR
from dateutil.relativedelta import relativedelta as delta
AMONTH = delta(months=1)
ADAY = delta(days=1)

from lino.utils.format_date import fds

DateRangeValue = collections.namedtuple(
    'DateRangeValue', ('start_date', 'end_date'))
"""
A named tuple with the following fields:

.. attribute:: start_date

    The start date

.. attribute:: end_date

    The end date
"""


def weekdays(start_date, end_date):
    """Return the number of weekdays that fall in the given period. Does
    not care about holidays.

    Usage examples in: :doc:`/topics/datetime`.

    """
    return len(list(rrule(
        DAILY, dtstart=start_date, until=end_date,
        byweekday=(MO, TU, WE, TH, FR))))



def daterange_text(a, b):
    """
    """
    if a == b:
        return fds(a)
    return fds(a) + "-" + fds(b)
