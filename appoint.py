def _calc_td(a):
    from datetime import datetime, timedelta, time
    return (datetime(a[0].year+a[4][0], a[0].month, a[0].day, a[0].hour,
        a[0].minute)-a[0])+timedelta(a[4][1], 3600*a[4][2]+60*a[4][3])

class appoint:
    from datetime import datetime, timedelta, time
    from . import special
    start = None
    end = None
    inc = None
    prio = None
    text = None
    spec = None

    def __init__(self, start, end, prio, inc, text, spec):
        self.start = start
        self.end = end
        self.inc = inc
        self.prio = prio
        self.text = text
        self.spec = spec

    def is_present(self, curr_time):
        return self.start <= curr_time and curr_time <= self.end
    def is_past(self, curr_time):
        return self.end < curr_time
    def is_future(self, curr_time):
        return curr_time < self.start

    def is_near(self, curr_time, time_eps):
        return curr_time < self.start and self.start <= curr_time + time_eps

    def evolve(self):
        """Generate the next occurence or None if there's none"""
        if not spec.has_next() or _calc_td(self.inc) == timedelta():
            return None
        self.spec.evolve()
        self.start = self.start + _calc_td(self.inc)
        self.end = self.end + _calc_td(self.inc)
        return self

    def to_tuple(self, curr_date):
        """Generate a tuple (start minute, end minute, prio, spec) \
                for a given date curr_date"""
        if not self.is_present(curr_date):
            return None
        return (self.start.hour*60+self.start.minute if
                self.start.date()==curr_date.date() else -1,
                self.end.hour*60+self.end.minute if
                self.end.date()==curr_date.date() else 1440 if
                self.end.time()==time(23,59) else 1500,
                self.prio,
                (self.text,self.spec))

