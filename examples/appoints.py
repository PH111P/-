# appoints.py: powerline segment
# Displays current and upcoming appointments and evolves them if necessary.

from __future__ import (unicode_literals, division, absolute_import, print_function)
from datetime import (datetime, timedelta)
from appoints import (appoint, special, io)
import os

def appoint(pl, count=1, time_before={"0":0, "1":30}, file_path=os.path.expanduser('~') + '/.appointlist'):
    '''Return the next ``count`` appoints
    :param int count:
        Number of appoints that shall be shown
    :param time_before:
        Time in minutes before the appoint to start alerting
    Highlight groups used: ``appoint``, ``appoint_urgent``.
    '''

    appoints = io.read_appoints(file_path)
    if appoints == None:
        return None

    appoints = {prio: [ap for ap in appoints if ap.prio == prio]
            for prio in range(0, max([0]+[b.prio for b in appoints])+1)}

    if appoints == None or len(appoints) == 0:
        return None

    now = datetime.now()

    #split into upcoming, current, past events, and events in the far future
    far_away = {prio:[] for prio in appoints.keys()}
    upcoming = {prio:[] for prio in appoints.keys()}
    current = {prio:[] for prio in appoints.keys()}

    time_before = {int(a):int(time_before[a]) for a in time_before}

    lst = 0
    for i in range(0, 1+max(appoints.keys())):
        if i in time_before:
            lst = time_before[i]
        else:
            time_before[i] = lst

    keys = appoints.keys()
    while len(appoints) != 0:
        for i in keys:
            if not i in appoints:
                appoints[i] = []
        far_away = {prio:far_away[prio]+[a for a in appoints[prio]
            if a.is_future(now)
            and not a.is_near(now,timedelta(0,time_before[prio]*60))]
            for prio in keys}
        upcoming = {prio:upcoming[prio]+[a for a in appoints[prio]
            if a.is_near(now,timedelta(0,time_before[prio]*60))]
            for prio in keys}
        current = {prio:current[prio]+[a for a in appoints[prio]
            if a.is_present(now)]
            for prio in keys}
        past = {prio:[a for a in appoints[prio]
            if a.is_past(now)]
            for prio in keys}

        appoints = {prio:[a.evolve() for a in past[prio]
            if a.evolve() != None]
            for prio in past.keys()}
        appoints = {prio:appoints[prio] for prio in appoints.keys()
                if appoints[prio] != []}

    keys = [k for k in keys]
    keys.sort()
    keys.reverse()
    result = []
    def prepend_space(str):
        if str == '':
            return ''
        return ' ' + str
    for k in keys:
        result += [{
            'contents': a.text+prepend_space(a.spec.print()),
            'highlight_groups': ['appoint_urgent']
            } for a in upcoming[k]]
    for k in keys:
        result += [{
            'contents': a.text+prepend_space(a.spec.print()),
            'highlight_groups': ['appoint']
            } for a in current[k]]

    #Write the changed appoints

    tw = []
    for k in keys:
        tw += current[k]
        tw += upcoming[k]
        tw += far_away[k]

    io.write_appoints(tw, file_path)

    if result != []:
        return [result[i] for i in range(0,min(len(result),count))]
    return None
