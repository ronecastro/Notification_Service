#!./venv/bin/python
"""Useful functions."""

from epics import PV, cainfo
from classes import NotificationInfoByPV
import symbols, json, re
from time import sleep
from copy import deepcopy
from datetime import datetime, timedelta
from json import dumps, loads
from db import App_db, FullPVList
from iofunctions import current_path as cpath, write
from modem_usb import Modem
from multiprocessing import Process, Value
from ctypes import c_bool
from psutil import process_iter
from datetime import datetime as dt

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


def makepvlist(fullpvlist, app_notifications):
    """Returns a lisf of string PV names, without duplicates."""
    try:
        pvlist = []
        notifications_raw = app_notifications.get()
        for item in notifications_raw:
            item = row2dict(item)
            i = 0
            n = json.loads(json.dumps(item))
            notification = json.loads(n[symbols.notification])
            for key in notification[symbols.notificationCores]:
                nC = symbols.notificationCore + str(i)
                comp_regex = re.compile(symbols.BGNCHAR + key[nC][symbols.pv + str(i)] + symbols.ENDCHAR)
                filterlist = list(filter(comp_regex.match, fullpvlist))
                for pv in filterlist:
                    if pv not in pvlist:
                        pvlist.append(pv)
                i += 1
    except Exception as e:
        print('Error on making PV list: ', e)
    return pvlist


def makepvpool(fullpvlist, app_notifications):
    """Returns a lisf of NotoficationInfoByPV classes."""
    pvpool = []
    notifications_db = app_notifications #App_db(symbols.Notifications)
    notifications_raw = symbols.notifications_raw
    j = 0
    for item in notifications_raw:
        i = 0
        n = str(item.get(symbols.notification))
        notification = json.loads(n)
        for core in notification[symbols.notificationCores]:
            nC = symbols.notificationCore + str(i)
            comp_regex = re.compile(symbols.BGNCHAR + core[nC][symbols.pv + str(i)] + symbols.ENDCHAR)
            filterlist = list(filter(comp_regex.match, fullpvlist))
            lim = symbols.limit + str(i)
            for element in filterlist:
                pvinfo = NotificationInfoByPV()
                pvinfo.notification_id = item[symbols.id]
                for nc in core.keys():
                    pvinfo.notificationCore = int(nc[-1])
                pvinfo.user_id = item[symbols.user_id]
                pvinfo.pv = element
                if core[nC].get(lim) is not None:
                    pvinfo.limit = core[nC][symbols.limit + str(i)]
                else:
                    pvinfo.limitLL = core[nC][symbols.limitLL + str(i)]
                    pvinfo.limitLU = core[nC][symbols.limitLU + str(i)]
                pvinfo.rule = core[nC][symbols.rule + str(i)]
                pvinfo.subrule = core[nC][symbols.subrule + str(i)]
                pvpool.append(pvinfo)
            i += 1
        j += 1
    return pvpool


def connect_pvs(allpvs, pvs_dict):
    # build up pv dictionary
    for pvname in allpvs:
        # if pv not in dictionary
        if pvname not in pvs_dict:
            # add to dictionary
            pvs_dict[pvname] = PV(pvname)
    # clean up unused PV objects
    for key in pvs_dict:
        # if dictionary key name not in list
        if key not in allpvs:
            # delete dictionary key
            del pvs_dict[key]


def get_enum_list(pv):
    ans3 = ''
    try:
        ans = cainfo(str(pv), print_out=True)
        if ans != '' and ans != None and 'enum strings:' in ans:
            ans2 = (ans.split('enum strings:')[-1])
            ans3 = ans2.split('\n')[1:-2]
        else:
            return
    except Exception as e:
        # print('e', e)
        return 'PV data not available'
    aux = []
    if ans3 != '' and ans3 is not None:
        for element in ans3:
            aux3 = element.strip()
            aux4 = aux3.replace(' ', '')
            aux5 = aux4.replace('\n', '')
            aux6 = aux5.replace('\t', '')
            aux7 = aux6.replace('\r', '')
            aux8 = aux7.replace('=', ' = ')
            aux.append(aux8)
        aux = '\n'.join(aux)
        if type(aux) == str:
            return aux
        else:
            return None
    else:
        return None


def post_test_notification(n, pvs_dict):
    """test if notification rules evaluates to true."""
    fullpvlist = list(pvs_dict.keys())
    notification = n[symbols.notification]
    notification_json = json.loads(notification)
    nc = notification_json[symbols.notificationCores]
    test_results = {"send_sms":False, "sizetrue": 0, "faulty":None, "pvs":{}}
    L, LL, LU = None, None, None
    complete_rule = []
    faulty = []
    try:
        for core in nc:
            rule_array = []
            true_pvs = {}
            true_pvs_array = []
            partial_rule = ""
            core_number = list(core.keys())[0].split("notificationCore", 1)[1]
            core_inner = core[symbols.notificationCore + core_number]
            pv_in_notification = (core_inner[symbols.pv + core_number]).strip()
            comp_regex = re.compile("^" + pv_in_notification + "$")
            pvnames = list(filter(comp_regex.match, fullpvlist))
            rule = core_inner[symbols.rule + core_number]
            subrule = core_inner[symbols.subrule + core_number]
            if (symbols.limit + core_number) in core_inner.keys():
                L = float(core_inner[symbols.limit + core_number])
            if (symbols.limitLL + core_number) in core_inner.keys():
                LL = float(core_inner[symbols.limitLL + core_number])
            if (symbols.limitLU + core_number) in core_inner.keys():
                LU = float(core_inner[symbols.limitLU + core_number])
            i = 0
            for pvname in pvnames:
                try:
                    if pvs_dict[pvname].connected:
                        pv = pvs_dict[pvname].value
                        try:
                            float(str(pv))
                        except:
                            rule_array.append(str(False))
                            faulty.append(pvname)
                            continue
                        eval_partial = eval(rule)
                        if eval_partial:
                            true_pvs.update({"pv" : pvname})
                            true_pvs.update({"value" : pv})
                            true_pvs.update({"rule" : rule})
                            true_pvs.update({"limit" : L})
                            true_pvs.update({"limitLL" : LL})
                            true_pvs.update({"limitLU" : LU})
                            true_pvs.update({"subrule" : subrule})
                            aux = deepcopy(true_pvs)
                            true_pvs_array.append(aux)
                            test_results["sizetrue"] += 1
                        rule_array.append(str(eval_partial))
                    else:
                        faulty.append(pvname)
                except Exception as e:
                    print("Error on PV test: ", e)
                    faulty.append(pvname)
                    rule_array.append(str(False))

            partial_rule = " or ".join(rule_array)
            partial_rule = eval(partial_rule)

            complete_rule.append(str(partial_rule))
            complete_rule.append(subrule.lower()) if subrule != '' else None
            test_results["pvs"].update({
                (pv_in_notification + "(" + core_number + ")") : true_pvs_array})
            if subrule != '':
                test_results.update({(symbols.subrule + core_number) : subrule})
            L, LL, LU = None, None, None
        if eval(" ".join(complete_rule)):
            test_results.update({"send_sms" : True})

        test_results.update({"faulty" : faulty})
    except Exception as e:
        print("Error on utils.py, post_test_notification function: ", e)

    return test_results


def sms_formatter(sms_text, ndata=None):
    """format SMS message text to sent to modem."""
    if sms_text:
        return sms_text + "\r\n"
    else:
        msg = "WARNING!\r\n"
        # print(ndata)
        if ndata["sizetrue"] <= 2:
            for key in ndata["pvs"]:
                aux = ndata["pvs"][key]
                if aux:
                    pvname = ndata["pvs"][key][0]["pv"]
                    pvvalue = ndata["pvs"][key][0]["value"]
                    rule = ndata["pvs"][key][0]["rule"]
                    subrule = ndata["pvs"][key][0]["subrule"]
                    msg += pvname + " = " + str(pvvalue) + "\r\n"
                    msg +="Rule: " + rule + "\r\n"
                    if ndata["pvs"][key][0]["limit"]:
                        msg += "Limit: " + str(ndata["pvs"][key][0]["limit"]) + "\r\n"
                    else:
                        msg += "LL: " + str(ndata["pvs"][key][0]["limitLL"]) + "\r\n"
                        msg += "LU: " + str(ndata["pvs"][key][0]["limitLL"]) + "\r\n"
                    if subrule:
                        msg += "Subrule: " + subrule + "\r\n"
            return msg
        else:
            msg += "Multiple PVs reached their limits!\r\n"
            for key in ndata["pvs"]:
                pvname = ndata["pvs"][key][0]["pv"]
                pvvalue = ndata["pvs"][key][0]["value"]
                rule = ndata["pvs"][key][0]["rule"]
                break
            msg += "First PV: " + pvname + "\r\n"
            msg += "Value: " + str(pvvalue) + "\r\n"
            msg += "Rule: " + rule + "\r\n"
            return msg


def show_running(loop_index):
    """show running status on prompt."""
    run = ["|", "/", "-", "\\", "|", "/", "-", "\\"]
    idx = loop_index % 8
    print(run[idx], end='\r')


def pre_test_notification(n, now):
    """test if notification can be sent."""
    can_send = False
    interval_can_send = False
    persistence_can_send = False
    expiration_can_send = False
    last_sent = n["last_sent"]
    n_lastsent = last_sent
    # if n_lastsent != None:
    #     pass
    # else:
    #     n_lastsent = None
    n_notification = loads(n["notification"])
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
    return can_send


def byebye(ans, n, now, app_notifications, users_db, update_db=True, update_log=True, no_text=False, send=True, print_msg=True, queue=None):
    try:
        user_id = n["user_id"]
        user = users_db.get(field="id", value=user_id)
        # get sms text from notification
        sms_text = n["sms_text"]
        # if no text option enabled
        if no_text:
            # set sms text to empty
            sms_text = ""
        # format sms text
        text2send = sms_formatter(sms_text, ndata=ans)
        # set cellphone number
        number = user.phone
        username = user.username

        # update notification last_sent key
        if update_db:
            n_id = n["id"]
            update_db_ans = app_notifications.update(n_id, "last_sent", now)
            # update log.txt

        # create variable to store data passed to new process
        basket = [number, text2send, update_db_ans, update_log, username, send, now, print_msg]
        # append data to queue
        queue.append(basket)
    except Exception as e:
        print("Error on utils.py, byebye function: ", e)

def prepare_evaluate(f, test_mode=False):
    if test_mode:
        try:
            fullpvlist = f.getlist()
            print("Full PV List created")
            modem = None
            print("Modem not created")
            print("USB Modem not initialized")
        except Exception as e:
            print("Error on prepare_evaluate function: ", e)
            exit()
    else:
        try:
            f.update()
            fullpvlist = f.getlist()
            print("Full PV List created")
            modem = Modem(debug=False)
            print("Modem object created")
            modem.initialize()
            print("USB Modem initialized")
            modem.closeconnection()
        except Exception as e:
            print("Error on prepare_evaluate function: ", e)
            exit()
    return fullpvlist, modem


def call_modem(number, text2send, update_db_ans, update_log, username, send, now, print_msg, busy):
    # initially, busy variable is True, because modem will be in use
    if send:
        modem = Modem()
        modem_ans = modem.sendsms(number=number, msg=text2send, force=True)
        modem.closeconnection()
        m_now = dt.now()
    else:
        modem_ans = 1
        m_now = dt.now()
    # if modem answer ok, proceed to write log
    if modem_ans:
        if update_db_ans and update_log:
            now = now.strftime("%Y-%m-%d %H:%M:%S")
            m_now = m_now.strftime("%Y-%m-%d %H:%M:%S")
            logmsg = now + " - SMS to " + str(username) + " at " + m_now + " with message: \r\n" + text2send + "\r\n"
            w_log = write("log.txt", logmsg)
            if print_msg:
                print(logmsg)
    else:
        if update_log:
            now = now.strftime("%Y-%m-%d %H:%M:%S")
            m_now = now.strftime("%Y-%m-%d %H:%M:%S")
            logmsg = now + " - SMS to " + str(username) + " was not sent due to modem error, at " + m_now + "\r\n"
            w_log = write("log.txt", logmsg)
            if print_msg:
                print(logmsg)

    # set busy variable to False, freeing the modem for next use
    sleep(1)
    busy.value = False
    return w_log


def sms_queuer(queue, busy, exit):
    while True:
        if len(queue) > 0 and not busy.value:
            call_modem_open = process_status("ns_call_modem")
            if not call_modem_open:
                basket = deepcopy(queue[0])
                queue.pop(0)
                number = basket[0]
                text2send = basket[1]
                update_db_ans = basket[2]
                update_log = basket[3]
                user = basket[4]
                send = basket[5]
                now = basket[6]
                print_msg = basket[7]
                busy.value = True
                proc = Process(target=call_modem, args=(number, text2send, update_db_ans, update_log, user, send, now, print_msg, busy), name="ns_call_modem")
                proc.start()
        sleep(1)
        if exit.value == True:
            exit()


def process_status(process_name):
    for process in process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            return True
    return False


# test_result = "{'send_sms': True, 'faulty': [], 'TS-04:PU-InjSeptG-1:Voltage-Mon(0)': ['TS-04:PU-InjSeptG-1:Voltage-Mon(407.7669430097902)'], 'subrule0': 'OR', 'TS-04:PU-InjSeptG-2:Voltage-Mon(1)': ['TS-04:PU-InjSeptG-2:Voltage-Mon(405.91594983988387)']}"
# sms_text = ""
# sms_formatter(sms_text, test_result)
