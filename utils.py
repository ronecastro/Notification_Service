#!./venv/bin/python
"""Useful functions."""

from db import App_db, FullPVList
from epics import PV, cainfo
from classes import NotificationInfoByPV
import symbols, json, re



def makepvlist(fullpvlist):
    """Returns a lisf of string PV names, without duplicates."""
    pvlist = []
    # f = FullPVList()
    # fullpvlist = f.getlist()
    notifications_db = App_db(symbols.Notifications)
    # notifications_raw = notifications_db.get()
    notifications_raw = symbols.notifications_raw
    for item in notifications_raw:
        i = 0
        n = str(item.get(symbols.notification))
        notification = json.loads(n)
        for key in notification[symbols.notificationCores]:
            nC = symbols.notificationCore + str(i)
            comp_regex = re.compile(symbols.BGNCHAR + key[nC][symbols.pv + str(i)] + symbols.ENDCHAR)
            filterlist = list(filter(comp_regex.match, fullpvlist))
            # print('filterlist', filterlist)
            for pv in filterlist:
                if pv not in pvlist:
                    pvlist.append(pv)
                    # lista com 10 elementos, para testes
                    # eliminar na versão final
                    # if len(pvlist) == 10:
                    #     return pvlist
            i += 1
    return pvlist


def makepvpool(fullpvlist):
    """Returns a lisf of NotoficationInfoByPV classes."""
    pvpool = []
    notifications_db = App_db(symbols.Notifications)
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
        ans = cainfo(pv, print_out=False, timeout=2)
        if ans != '' and ans != None and 'enum strings:' in ans:
            ans2 = (ans.split('enum strings:')[-1])
            ans3 = ans2.split('\n')[1:-2]
        else:
            return
    except Exception as e:
        #print('e', e)
        return
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
    test_results = {"send_sms" : False, "faulty" : None}
    L, LL, LU = None, None, None
    complete_rule = []
    faulty = []
    for core in nc:
        rule_array = []
        true_pvs = []
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
        for pvname in pvnames:
            try:
                if pvlist_dict[pvname].connected:
                    pv = str(pvlist_dict[pvname].value)
                    rule4eval = re.sub("pv", pv, rule)
                    rule4eval = re.sub("L$", str(L), rule4eval)
                    rule4eval = re.sub("LL", str(LL), rule4eval)
                    rule4eval = re.sub("LU", str(LU), rule4eval)
                    eval_partial = eval(rule4eval)
                    if eval_partial:
                        true_pvs.append(pvname)
                    rule_array.append(str(eval_partial))
                else:
                    faulty.append(pvname)
            except Exception as e:
                faulty.append(pvname)
                rule_array.append(str(False))

        partial_rule = " or ".join(rule_array)
        partial_rule = eval(partial_rule)

        complete_rule.append(str(partial_rule))
        complete_rule.append(subrule.lower()) if subrule != '' else None
        test_results.update({(pv_in_notification + "(" + core_number + ")") : true_pvs})
        if subrule != '':
            test_results.update({(symbols.subrule + core_number) : subrule})
    if eval(" ".join(complete_rule)):
        test_results.update({"send_sms" : True})

    test_results.update({"faulty" : faulty})

    return test_results
