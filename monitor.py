#!./venv/bin/python
from db import App_db, FullPVList
from utils import makepvlist, connect_pvs, test_notification, sms_formatter, show_running
from epics import PV
from time import sleep
from symbols import *
from datetime import datetime, timedelta
from json import dumps, loads
from modem_usb import Modem
from iofunctions import current_path as cpath, write
from os import path

def evaluate():
    f = FullPVList()
    # f.update()
    fullpvlist = f.getlist()
    # k = 0
    # m = Modem(debug=False)
    # m.initialize()
    loop_index = 0
    print("Running!")
    while True: # k = 0
        try:
            # k = 1
            app_notifications = App_db("notifications")
            allpvs = makepvlist(fullpvlist, app_notifications)

            pvlist = connect_pvs(allpvs)
            pvlist_dict = {}
            pvlist_str = []
            for pv in pvlist:
                pvlist_str.append(pv.pvname)
                pvlist_dict[pv.pvname] = pv

            notifications_raw = app_notifications.get()
            now = datetime.now()
            for n in notifications_raw:
                can_send = False
                interval_can_send = False
                persistence_can_send = False
                expiration_can_send = False
                last_sent = n["last_sent"]
                if last_sent != None:
                    n_lastsent = n["last_sent"]
                else:
                    n_lastsent = None
                n_notification = loads(n[notification])
                n_id = n[id]
                n_created = datetime.strptime(n_notification["created"], '%Y-%m-%d %H:%M')
                n_interval = timedelta(minutes=int(n_notification["interval"]))
                n_persistence = n_notification["persistence"]
                n_expiration = datetime.strptime(n_notification["expiration"], '%Y-%m-%d %H:%M')
                # test interval:
                if n_lastsent != None:
                    if now >= (n_lastsent + n_interval):
                        interval_can_send = True
                else:
                    interval_can_send = True
                # test persistence:
                if n_persistence == 'NO':
                    if n_lastsent == None:
                        persistence_can_send = True
                else:
                    persistence_can_send = True
                # test expiration
                if now <= n_expiration:
                    expiration_can_send = True

                # if all conditions outside notification
                if interval_can_send == True and \
                    persistence_can_send == True and \
                    expiration_can_send == True:
                    can_send = True

                if can_send:
                    # test conditions inside notification (rules)
                    ans = test_notification(n, pvlist_dict, fullpvlist)
                    if ans["send_sms"]:
                        user_id = n["user_id"]
                        users_db = App_db(users)
                        user = users_db.get(field=id, value=user_id)
                        sms_text = "" #n["sms_text"] <=========================
                        text2send = sms_formatter(sms_text, ndata=ans)
                        print(loop_index)
                        print(text2send)
                        r = 1 # = m.sendsms_force(number=user.phone, msg=text2send)
                        if r == 1:
                            # update notification last_sent key
                            # app_notifications.update(n_id, "last_sent", now)
                            now = now.strftime("%Y-%m-%d %H:%M:%S")
                            logmsg = now + " - SMS to " + user.username + " with message: \n\r" + text2send + "\r\n"
                            write("log.txt", logmsg)
        except KeyboardInterrupt:
            break

        loop_index = show_running(loop_index) # printing running sign

        sleep(0.2)


evaluate()

# users_db = App_db(users)
# u = users_db.get(field="id", value=7)
# print(u.phone)
# print(user_id)
# print(phone)

# f = FullPVList()
# fullpvlist = f.getlist()
# print(f.is_pv_on_list("RAD:Berthold:TotalDoseRate:Dose"))
