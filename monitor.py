#!./venv/bin/python
from utils import makepvlist, connect_pvs, post_test_notification, pre_test_notification, show_running, byebye, prepare_evaluate
from epics import PV
from time import sleep
from symbols import *
from os import path
from datetime import datetime as dt
from db import App_db, FullPVList

def evaluate():
    # make full PV list and create modem object
    f = FullPVList()
    fullpvlist, modem = prepare_evaluate(f, test_mode=False)
    loop_index = 0
    print("Running!")
    while True:
        try:
            # load notification db
            app_notifications = App_db("notifications")
            # create pv list with all pvs used in db
            allpvs = makepvlist(fullpvlist, app_notifications)
            # create list of PV objects
            pvlist = connect_pvs(allpvs)
            # create dictionary from pv list
            pvlist_dict = {pv.pvname : pv for pv in pvlist}
            # get notifications from db
            notifications_raw = app_notifications.get()
            now = dt.now()
            # for each notification
            for n in notifications_raw:
                #test condition outside notification rules
                can_send = pre_test_notification(n, now)
                if can_send:
                    # test conditions inside notification rules
                    ans = post_test_notification(n, pvlist_dict, fullpvlist)
                    if ans["send_sms"]:
                        # send SMS to phone number and write to log.txt
                        users_db = App_db("users")
                        r = byebye(ans, n, now, app_notifications, users_db, modem, update_db=False, update_log=True, no_text=True, send=False)
        except KeyboardInterrupt:
            break
        # print 'running' symbol each iteration
        loop_index = show_running(loop_index) # printing running sign
        sleep(0.1)


evaluate()

# users_db = App_db(users)
# u = users_db.get(field="id", value=7)
# print(u.phone)
# print(user_id)
# print(phone)

# f = FullPVList()
# fullpvlist = f.getlist()
# print(f.is_pv_on_list("RAD:Berthold:TotalDoseRate:Dose"))
