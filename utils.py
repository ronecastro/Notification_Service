#!./venv/bin/python
"""Useful functions."""

from epics import PV, cainfo
from classes import NotificationInfoByPV
import symbols, json, re



def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


def makepvlist(fullpvlist, app_notifications):
    """Returns a lisf of string PV names, without duplicates."""
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


def connect_pvs(pvlist):
    pvs = [PV(pvname) for pvname in pvlist]
    for pv in pvs:
        pv.wait_for_connection(timeout=2)
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

def test_notification(n, pvlist_dict, fullpvlist):
    notification = n[symbols.notification]
    notification_json = json.loads(notification)
    nc = notification_json[symbols.notificationCores]
    test_results = {"send_sms":False, "sizetrue": 0, "faulty":None, "pvs":{}}
    L, LL, LU = None, None, None
    complete_rule = []
    faulty = []
    for core in nc:
        rule_array = []
        true_pvs = {}
        partial_rule = ""
        core_number = list(core.keys())[0][-1]
        core_inner = core[symbols.notificationCore + core_number]
        pv_in_notification = (core_inner[symbols.pv + core_number]).strip()
        comp_regex = re.compile(pv_in_notification)
        pvnames = list(filter(comp_regex.match, fullpvlist))
        rule = core_inner[symbols.rule + core_number]
        subrule = core_inner[symbols.subrule + core_number]
        if (symbols.limit + core_number) in core_inner.keys():
            L = core_inner[symbols.limit + core_number]
        if (symbols.limitLL + core_number) in core_inner.keys():
            LL = core_inner[symbols.limitLL + core_number]
        if (symbols.limitLU + core_number) in core_inner.keys():
            LU = core_inner[symbols.limitLU + core_number]
        i = 0
        for pvname in pvnames:
            try:
                if pvlist_dict[pvname].connected:
                    pv = str(round(pvlist_dict[pvname].value, 3))
                    rule4eval = re.sub("pv", pv, rule)
                    rule4eval = re.sub("L$", str(L), rule4eval)
                    rule4eval = re.sub("LL", str(LL), rule4eval)
                    rule4eval = re.sub("LU", str(LU), rule4eval)
                    eval_partial = eval(rule4eval)
                    if eval_partial:
                        true_pvs.update({"pv" : pvname})
                        true_pvs.update({"value" : pv})
                        true_pvs.update({"rule" : rule})
                        true_pvs.update({"limit" : L})
                        true_pvs.update({"limitLL" : LL})
                        true_pvs.update({"limitLU" : LU})
                        true_pvs.update({"subrule" : subrule})
                        test_results["sizetrue"] += 1
                    rule_array.append(str(eval_partial))
                else:
                    faulty.append(pvname)
            except Exception as e:
                print('error: ', e)
                faulty.append(pvname)
                rule_array.append(str(False))

        partial_rule = " or ".join(rule_array)
        partial_rule = eval(partial_rule)

        complete_rule.append(str(partial_rule))
        complete_rule.append(subrule.lower()) if subrule != '' else None
        test_results["pvs"].update({
            (pv_in_notification + "(" + core_number + ")") : true_pvs})
        if subrule != '':
            test_results.update({(symbols.subrule + core_number) : subrule})
        L, LL, LU = None, None, None
    if eval(" ".join(complete_rule)):
        test_results.update({"send_sms" : True})

    test_results.update({"faulty" : faulty})

    return test_results

def sms_formatter(sms_text, ndata=None):
    if sms_text:
        return sms_text
    else:
        msg = "WARNING!\r\n"
        for key in ndata["pvs"]:
            pvname = ndata["pvs"][key]["pv"]
            pvvalue = ndata["pvs"][key]["value"]
            rule = ndata["pvs"][key]["rule"]
            subrule = ndata["pvs"][key]["subrule"]
            msg += pvname + " = " + pvvalue + "\r\n"
            msg +="Rule: " + rule + "\r\n"
            if ndata["pvs"][key]["limit"]:
                msg += "Limit: " + ndata["pvs"][key]["limit"] + "\r\n"
            else:
                msg += "LL: " + ndata["pvs"][key]["limitLL"] + "\r\n"
                msg += "LU: " + ndata["pvs"][key]["limitLL"] + "\r\n"
            if subrule:
                msg += "Subrule: " + subrule + "\r\n"
        return msg

# test_result = "{'send_sms': True, 'faulty': [], 'TS-04:PU-InjSeptG-1:Voltage-Mon(0)': ['TS-04:PU-InjSeptG-1:Voltage-Mon(407.7669430097902)'], 'subrule0': 'OR', 'TS-04:PU-InjSeptG-2:Voltage-Mon(1)': ['TS-04:PU-InjSeptG-2:Voltage-Mon(405.91594983988387)']}"
# sms_text = ""
# sms_formatter(sms_text, test_result)
