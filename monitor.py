#!./venv/bin/python
from db import App_db, FullPVList
from utils import makepvlist, connect_pvs, test_notification, sms_formatter
from epics import PV
from time import sleep
from symbols import *
from datetime import datetime, timedelta
from json import dumps, loads
from modem_usb import Modem
from urllib import parse

def evaluate():
    f = FullPVList()
    # f.update()
    fullpvlist = f.getlist()
    k = 0
    # m = Modem(debug=True)
    # m.initialize()
    while k == 0: #True:
        try:
            k = 1
            app_notifications = App_db(Notifications)
            allpvs = makepvlist(fullpvlist, app_notifications)
            # f = open('test.txt')
            # allpvs = f.read()

            pvlist = connect_pvs(allpvs)
            pvlist_dict = {}
            pvlist_str = []
            for pv in pvlist:
                pvlist_str.append(pv.pvname)
                pvlist_dict[pv.pvname] = pv

            # for pv in pvlist:
            #     if pv.connected:
            #         print(pv.pvname, pv.value)
            #     else:
            #         print(pv.pvname, 'NOT CONNECTED')

            notifications_db = App_db('notifications')
            # print(notifications_db.get())
            # notifications_raw = notifications_db.get()
            users_db = App_db(users)
            notifications = notifications_raw2
            now = datetime.now()
            for n in notifications:
                can_send = False
                interval_can_send = False
                persistence_can_send = False
                expiration_can_send = False
                if n["last_sent"] != None:
                    n_lastsent = n["last_sent"]
                else:
                    n_lastsent = None
                n_notification = loads(n[notification])
                n_created = datetime.strptime(n_notification["created"], '%Y-%m-%d %H:%M')
                n_interval = timedelta(minutes=int(n_notification["interval"]))
                n_persistence = n_notification["persistence"]
                n_expiration = datetime.strptime(n_notification["expiration"], '%Y-%m-%d %H:%M')
                # test interval:
                if n_lastsent != None:
                    if now >= (n_lastsent + n_interval):
                        interval_can_send = True
                else:
                    if now >= (n_created + n_interval):
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
                    print(ans)
                    if ans["send_sms"]:
                        user_id = n["user_id"]
                        user = users_db.get(field=id, value=user_id)
                        sms_text = n["sms_text"]
                        sms_text = ""
                        print(sms_formatter(sms_text, test_results=ans, n=n))
                        # r = m.sendsms_force(number=user.phone, msg=sms_text)[0]
                        r = 'ok'
                        if r == 'ok':
                            # update notification last_sent key
                            # notifications_db.update(n[id], last_sent, now)
                            # print(notifications_db.get())
                            pass

        except KeyboardInterrupt:
            break
        sleep(1)


evaluate()

# users_db = App_db(users)
# u = users_db.get(field="id", value=7)
# print(u.phone)
# print(user_id)
# print(phone)

# f = FullPVList()
# fullpvlist = f.getlist()
# print(f.is_pv_on_list("RAD:Berthold:TotalDoseRate:Dose"))
