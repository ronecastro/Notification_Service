#!./venv/bin/python
from utils import makepvlist, connect_pvs, post_test_notification, pre_test_notification, show_running, byebye, prepare_evaluate
from epics import PV
from time import sleep
from symbols import *
from datetime import datetime as dt
from db import * #App_db, FullPVList
import os
from psutil import Process as ps_proc

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
            if isinstance(notifications_raw, Exception):
                print("Error on getting notifications DB: " , notifications_raw)
                break
            now = dt.now()
            # for each notification
            for n in notifications_raw:
                #test condition outside notification rules
                can_send = pre_test_notification(n, now)
                if can_send:
                    print(now, " - ", can_send)
                    # test conditions inside notification rules
                    ans = post_test_notification(n, pvlist_dict, fullpvlist)
                    print(ans)
                    if ans["send_sms"]:
                        # send SMS to phone number and write to log.txt
                        users_db = App_db("users")
                        update_db= True # update notification database
                        update_log = True # write to log.txt
                        no_text = False # force SMS text to none
                        send = False # send SMS through modem
                        r = byebye(ans, n, now, app_notifications, users_db, modem, update_db=update_db, update_log=update_log, no_text=no_text, send=send)
        except KeyboardInterrupt:
            break
        # print 'running' symbol each iteration
        loop_index = show_running(loop_index) # printing running sign
        sleep(0.15)

        me = ps_proc(os.getpid())
        if me.parent() is not None:
            continue
        else:
            break


evaluate()

# users_db = App_db(users)
# u = users_db.get(field="id", value=7)
# print(u.phone)
# print(user_id)
# print(phone)

# f = FullPVList()
# fullpvlist = f.getlist()
# print(f.is_pv_on_list("RAD:Berthold:TotalDoseRate:Dose"))
