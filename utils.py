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


def connect_pvs(pvlist, timeout=2):
    pvs = [PV(pvname) for pvname in pvlist]
    for pv in pvs:
        if pv.connected:
            sleep(0.015)
        else:
            pv.wait_for_connection(timeout=timeout)
            if pv.connected:
                sleep(0.015)
    return pvs


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

def post_test_notification(n, pvlist_dict, fullpvlist):
    """test if notification rules evaluates to true."""
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
                    if pvlist_dict[pvname].connected:
                        pv = pvlist_dict[pvname].value
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
                    print("Error on test: ", e)
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
        print('Error on PV test: ', e)

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
            msg += "More than 3 PVs reached their limits!\r\n"
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
    if loop_index == 0:
        print("|", end='\r')
    if loop_index == 1:
        print("/", end='\r')
    if loop_index == 2:
        print("-", end='\r')
    if loop_index == 3:
        print("\\", end='\r')
    if loop_index == 4:
        print("|", end='\r')
    if loop_index == 5:
        print("/", end='\r')
    if loop_index == 6:
        print("-", end='\r')
    if loop_index == 7:
        print("\\", end='\r')

    loop_index += 1
    if loop_index >= 8:
        loop_index = 0

    return loop_index


def pre_test_notification(n, now):
    """test if notification can be sent."""
    can_send = False
    interval_can_send = False
    persistence_can_send = False
    expiration_can_send = False
    last_sent = n["last_sent"]
    if last_sent != None:
        n_lastsent = n["last_sent"]
    else:
        n_lastsent = None
    n_notification = loads(n["notification"])
    n_id = n["id"]
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
    return can_send

def byebye(ans, n, now, app_notifications, users_db, modem, update_db=True, update_log=True, no_text=False, send=True):
    r = 0
    try:
        user_id = n["user_id"]
        user = users_db.get(field="id", value=user_id)
        sms_text = n["sms_text"]
        if no_text:
            sms_text = ""
        text2send = sms_formatter(sms_text, ndata=ans)
        if send:
            r = modem.sendsms_force(number=user.phone, msg=text2send)
        else:
            r = 1
        if r:
            # update notification last_sent key
            if update_db:
                n_id = n["id"]
                r = app_notifications.update(n_id, "last_sent", now)
                # update log.txt
            if r and update_log:
                now = now.strftime("%Y-%m-%d %H:%M:%S")
                logmsg = now + " - SMS to " + str(user.username) + " with message: \r\n" + text2send + "\r\n"
                r = write("log.txt", logmsg)
                print(logmsg)
        else:
            if update_log:
                now = now.strftime("%Y-%m-%d %H:%M:%S")
                logmsg = now + " - SMS to " + str(user.username) + " was not sent due to modem error" + "\r\n"
                r = write("log.txt", logmsg)
                print(logmsg)

        return r
    except Exception as e:
        print("Error on sending SMS: ", e)
        return r

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
        except Exception as e:
            print("Error on prepare_evaluate function: ", e)
            exit()
    return fullpvlist, modem


# test_result = "{'send_sms': True, 'faulty': [], 'TS-04:PU-InjSeptG-1:Voltage-Mon(0)': ['TS-04:PU-InjSeptG-1:Voltage-Mon(407.7669430097902)'], 'subrule0': 'OR', 'TS-04:PU-InjSeptG-2:Voltage-Mon(1)': ['TS-04:PU-InjSeptG-2:Voltage-Mon(405.91594983988387)']}"
# sms_text = ""
# sms_formatter(sms_text, test_result)
