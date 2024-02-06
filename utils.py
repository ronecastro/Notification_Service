#!./venv/bin/python
from db import App_db
from epics import PV
import symbols, json, re


def makepvlist(fullpvlist):
    pvlist = []
    notifications_db = App_db(symbols.notifications)
    notifications_raw = notifications_db.get()
    for item in notifications_raw:
        i = 0
        n = str(item.notification)
        notification = json.loads(n)
        for key in notification[symbols.notificationCores]:
            nC = symbols.notificationCore + str(i)
            if i > 0:
                comp_regex = re.compile(key[nC][symbols.pv + str(i)])
                filterlist = list(filter(comp_regex.match, fullpvlist))
                for pv in filterlist:
                    if pv not in pvlist:
                        pvlist.append(pv)
            else:
                comp_regex = re.compile(key[nC][symbols.pv])
                filterlist = list(filter(comp_regex.match, fullpvlist))
                for pv in filterlist:
                    if pv not in pvlist:
                        pvlist.append(pv)
            i += 1
    return pvlist

def connect_pvs(pvlist):
    pvs = [PV(pvname) for pvname in pvlist]
    for pv in pvs:
        pv.wait_for_connection()
    return pvs
