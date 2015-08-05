def _calc_td(start, inc):
    from datetime import datetime, timedelta, time
    return (datetime(start.year+inc[0], start.month, start.day, start.hour,
        start.minute)-start)+timedelta(inc[1], 3600*inc[2]+60*inc[3])

def _enc_dt(dt):
    import random
    lns = dt.strftime('%Y %m %d %H %M').split()
    res = lns[0]
    for i in range(1, len(lns)):
        res += str(random.randint(0,9)) + lns[i]
    return res
def _dec_dt(dt):
    from datetime import datetime
    return datetime(int(dt[0:4]),
            int(dt[5:7]),
            int(dt[8:10]),
            int(dt[11:13]),
            int(dt[14:16]))

def _enc_inc(inc, prio):
    import random
    res = str(prio) + ' '
    for i in inc:
        res += str(i) + ' '
    res += str(random.randint(1<<50,1<<128))[0:16-len(res)]
    return res
def _dec_inc(str):
    tmp = str.split()
    return ([int(tmp[i]) for i in [1, 2, 3, 4]], int(tmp[0]))

class appoint:
    from datetime import datetime, timedelta, time
    from . import special
    start = None
    end = None
    inc = None
    prio = None
    text = None
    spec = None

    def __init__(self, start, end, prio, inc, text, spec, data=None):
        if data == None:
            self.start = start
            self.end = end
            self.inc = inc
            self.prio = prio
            self.text = text
            self.spec = spec
        else:
            self.start = _dec_dt(data[0])
            self.end = _dec_dt(data[1])
            tm = _dec_inc(data[2])
            self.inc = tm[0]
            self.prio = tm[1]

    def is_present(self, curr_time):
        return self.start <= curr_time and curr_time <= self.end
    def is_past(self, curr_time):
        return self.end < curr_time
    def is_future(self, curr_time):
        return curr_time < self.start

    def is_near(self, curr_time, time_eps):
        return curr_time < self.start and self.start <= curr_time + time_eps

    def is_present_on_day(self, date):
        return self.start.date() <= date.date()\
                and date.date() <= self.end.date()

    def evolve(self):
        """Generate the next occurence or None if there's none"""
        from datetime import timedelta
        if not self.spec.has_next()\
            or _calc_td(self.start, self.inc) == timedelta():
            return None
        spec = self.spec.evolve()
        start = self.start + _calc_td(self.start, self.inc)
        end = self.end + _calc_td(self.start, self.inc)
        return appoint(start, end, self.prio, self.inc, self.text, spec)

    def to_tuple(self, curr_date):
        """Generate a tuple (start minute, end minute, prio, spec) \
                for a given date curr_date"""
        if not self.is_present_on_day(curr_date):
            return None
        return (self.start.hour*60+self.start.minute if
                self.start.date()==curr_date.date() else -1,
                self.end.hour*60+self.end.minute if
                self.end.date()==curr_date.date() else 1440 if
                self.end.time()==time(23,59) else 1500,
                self.prio,
                (self.text,self.spec))

    def to_bytes(self):
        res = [_enc_dt(self.start).encode(),
                _enc_dt(self.end).encode(),
                _enc_inc(self.inc, self.prio)[0:16].encode()]
        return res

