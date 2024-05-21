#!./venv/bin/python

all = 'all'
ALL = '"all"'
id = 'id'
users = 'users'
Users = 'Users'
Notification = 'Notification'
notification = 'notification'
Notifications = 'Notifications'
notifications = 'notifications'
notificationCore = 'notificationCore'
notificationCores = 'notificationCores'
expiration = 'expirations'
limit = 'limit'
limitLL = 'limitLL'
limitLU = 'limitLU'
rule = 'rule'
rules = 'rules'
subrule = 'subrule'
user_id = 'user_id'
notification_id = 'notification_id'
rule_id = 'rule_id'
username = 'username'
email = 'email'
phone = 'phone'
rule = 'rule'
sms_text = 'sms_text'
last_sent = 'last_sent'
app_db = 'app.db'
fullpvlist_db = 'fullpvlist.db'
pv = "pv"
BGNCHAR = '^'
ENDCHAR = '$'

### USB 3G MODEM ###
usbmodemport = '/dev/ttyUSB0'
LF = chr(10) #\n
CR = chr(13) #\r
SUB = chr(26)
EOMM = chr(26) #End of Messsage Marker
ATE0 = 'ATE0' + CR
ATE1 = 'ATE1' + CR
ATZ = 'ATZ' + CR
CMEE_1 = 'AT+CMEE=1' + CR
CMEE_0 = 'AT+CMEE=0' + CR
CMGF_1 = 'AT+CMGF=1' + CR
CMGW = 'AT+CMGW='
CMSS = 'AT+CMSS='
CPMS = 'AT+CPMS='
CMGD = 'AT+CMGD='
CMGS = 'AT+CMGS='
CSMP = 'AT+CSMP='
CNMI = 'AT+CNMI='
CMGL = 'AT+CMGL='

notifications_raw = \
[{'id': 1, 'user_id': 2, 'notification': '{"created": "2023-09-15 22:19", "expiration": "2023-11-30 23:59", "interval": "60", "persistence": "YES", "sms_msg" : "", "notificationCores": [{"notificationCore0": {"pv0": "SI-13C4:DI-DCCT:Current-Mon", "rule0": "pv < L", "limit0": "99.5", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 2, 'user_id': 2, 'notification': '{"created": "2023-09-15 22:19", "expiration": "2023-11-30 23:59", "interval": "60", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:AP-SOFB:LoopState-Sel", "rule0": "pv == L", "limit0": "0", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 3, 'user_id': 2, 'notification': '{"created": "2023-09-21 02:53", "expiration": "2023-11-30 23:59", "interval": "60", "persistence": "NO", "notificationCores": [{"notificationCore0": {"pv0": "^([ST][IBS])(.+VA-CCG.+Pressure-Mon)$", "rule0": "pv > L", "limit0": "1e-8", "subrule0": "OR"}}, {"notificationCore1": {"pv1": "^BO.+VA-CCG.+Pressure-Mon$", "rule1": "pv > L", "limit1": "1e-7", "subrule1": ""}}]}', 'last_sent': None},
{'id': 4, 'user_id': 4, 'notification': '{"created": "2023-09-15 22:27", "expiration": "2023-12-31 22:00", "interval": "60", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI.+CCG.+Pressure-Mon$", "rule0": "pv > L", "limit0": "1e-8", "subrule0": ""}}]}', 'last_sent': None},
{'id': 5, 'user_id': 4, 'notification': '{"created": "2023-09-15 22:28", "expiration": "2023-12-31 22:00", "interval": "60", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "BO.+CCG.+Pressure-Mon$", "rule0": "pv > L", "limit0": "1e-8", "subrule0": ""}}]}', 'last_sent': None},
{'id': 6, 'user_id': 4, 'notification': '{"created": "2023-09-15 22:28", "expiration": "2023-12-31 22:00", "interval": "60", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "TB.+CCG.+Pressure-Mon$", "rule0": "pv > L", "limit0": "1e-8", "subrule0": ""}}]}', 'last_sent': None},
{'id': 7, 'user_id': 4, 'notification': '{"created": "2023-09-15 22:29", "expiration": "2023-12-31 22:00", "interval": "60", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "TS.+CCG.+Pressure-Mon$", "rule0": "pv > L", "limit0": "1e-8", "subrule0": ""}}]}', 'last_sent': None},
{'id': 8, 'user_id': 4, 'notification': '{"created": "2023-09-15 22:29", "expiration": "2023-12-21 22:00", "interval": "60", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:AP-SOFB:LoopState-Sts", "rule0": "pv == L", "limit0": "0", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 9, 'user_id': 4, 'notification': '{"created": "2023-09-15 22:30", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "GEN-03:CO-SIMAR-01:Temp-Mon", "rule0": "pv > L", "limit0": "27", "subrule0": ""}}]}', 'last_sent': None},
{'id': 10, 'user_id': 4, 'notification': '{"created": "2023-09-15 22:32", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-13C4:DI-DCCT:Current-Mon", "rule0": "pv < L", "limit0": "99.5", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 11, 'user_id': 4, 'notification': '{"created": "2023-09-15 22:32", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:DI-BbBProc-H:FBCTRL", "rule0": "pv == L", "limit0": "0", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 12, 'user_id': 4, 'notification': '{"created": "2023-09-15 22:39", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:DI-BbBProc-V:FBCTRL", "rule0": "pv == L", "limit0": "0", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 13, 'user_id': 4, 'notification': '{"created": "2023-09-15 22:40", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:DI-BbBProc-L:FBCTRL", "rule0": "pv == L", "limit0": "0", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 14, 'user_id': 5, 'notification': '{"created": "2023-09-15 22:42", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI.+CCG.+Pressure-Mon$", "rule0": "pv > L", "limit0": "1e-8", "subrule0": ""}}]}', 'last_sent': None},
{'id': 15, 'user_id': 5, 'notification': '{"created": "2023-09-15 22:43", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "BO.+CCG.+Pressure-Mon$", "rule0": "pv > L", "limit0": "1e-8", "subrule0": ""}}]}', 'last_sent': None},
{'id': 16, 'user_id': 5, 'notification': '{"created": "2023-09-15 22:43", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "TB.+CCG.+Pressure-Mon$", "rule0": "pv > L", "limit0": "1e-8", "subrule0": ""}}]}', 'last_sent': None},
{'id': 17, 'user_id': 5, 'notification': '{"created": "2023-09-15 22:43", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "TS.+CCG.+Pressure-Mon$", "rule0": "pv > L", "limit0": "1e-8", "subrule0": ""}}]}', 'last_sent': None},
{'id': 18, 'user_id': 5, 'notification': '{"created": "2023-09-15 22:45", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:AP-SOFB:LoopState-Sel", "rule0": "pv == L", "limit0": "0", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 19, 'user_id': 5, 'notification': '{"created": "2023-09-15 22:46", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "RoomSrv:CO-SIMAR-01:AmbientTemp-Mon", "rule0": "pv > L", "limit0": "24", "subrule0": ""}}]}', 'last_sent': None},
{'id': 20, 'user_id': 5, 'notification': '{"created": "2023-09-15 22:48", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:AP-FOFB:LoopState-Sts", "rule0": "pv == L", "limit0": "0", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 21, 'user_id': 5, 'notification': '{"created": "2023-09-15 22:50", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:DI-BbBProc-L:FBCTRL", "rule0": "pv == L", "limit0": "0", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 22, 'user_id': 5, 'notification': '{"created": "2023-09-15 22:51", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:DI-BbBProc-V:FBCTRL", "rule0": "pv == L", "limit0": "0", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 23, 'user_id': 5, 'notification': '{"created": "2023-09-15 22:51", "expiration": "2023-12-21 22:00", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:DI-BbBProc-H:FBCTRL", "rule0": "pv == L", "limit0": "0", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 24, 'user_id': 5, 'notification': '{"created": "2023-09-15 22:52", "expiration": "2023-12-31 23:59", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-13C4:DI-DCCT:Current-Mon", "rule0": "pv < L", "limit0": "99.5", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 25, 'user_id': 9, 'notification': '{"created": "2023-09-16 05:48", "expiration": "2025-12-24 09:45", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "^RAD:Thermo.+:TotalDoseRate:Dose$", "rule0": "pv > L", "limit0": "1", "subrule0": "OR"}}, {"notificationCore1": {"pv1": "RAD:ELSE:TotalDoseRate:Dose$", "rule1": "pv > L", "limit1": "1", "subrule1": "OR"}}, {"notificationCore2": {"pv2": "RAD:Berthold:TotalDoseRate:Dose$ ", "rule2": "pv > L", "limit2": "1", "subrule2": ""}}]}', 'last_sent': None},
{'id': 26, 'user_id': 9, 'notification': '{"created": "2023-09-16 05:49", "expiration": "2025-12-24 13:00", "interval": "20", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-13C4:DI-DCCT:Current-Mon", "rule0": "pv < L", "limit0": "10", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 27, 'user_id': 6, 'notification': '{"created": "2023-09-16 05:52", "expiration": "2037-08-25 14:37", "interval": "30", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "^RAD:Thermo.+:TotalDoseRate:Dose$", "rule0": "pv >= L", "limit0": "1", "subrule0": "OR"}}, {"notificationCore1": {"pv1": "RAD:ELSE:TotalDoseRate:Dose", "rule1": "pv >= L", "limit1": "1", "subrule1": "OR"}}, {"notificationCore2": {"pv2": "RAD:Berthold:TotalDoseRate:Dose$", "rule2": "pv >= L", "limit2": "1", "subrule2": ""}}]}', 'last_sent': None},
{'id': 28, 'user_id': 6, 'notification': '{"created": "2023-09-16 05:53", "expiration": "2037-08-25 14:41", "interval": "30", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-13C4:DI-DCCT:Current-Mon", "rule0": "pv < L", "limit0": "10", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 29, 'user_id': 7, 'notification': '{"created": "2023-09-16 05:55", "expiration": "2023-12-29 19:20", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:AP-SOFB:LoopState-Sts", "rule0": "pv == L", "limit0": "0", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 30, 'user_id': 7, 'notification': '{"created": "2023-09-16 05:56", "expiration": "2023-12-29 22:10", "interval": "60", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "RA-RaSIA02:RF-IntlkCtrl:IntlkSirius-Mon", "rule0": "pv == L", "limit0": "1", "subrule0": "OR"}}, {"notificationCore1": {"pv1": "SI-Glob:AP-CurrInfo:Current-Mon", "rule1": "pv < L", "limit1": "5", "subrule1": ""}}]}', 'last_sent': None},
{'id': 31, 'user_id': 7, 'notification': '{"created": "2023-09-16 05:57", "expiration": "2023-12-29 23:00", "interval": "60", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-.+FE:VA-SIP150-.+:Current-Mon$", "rule0": "pv == L", "limit0": "0", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "SI-.+FE:VA-CCG-.+:Pressure-Mon$", "rule1": "pv > L", "limit1": "1e-10", "subrule1": ""}}]}', 'last_sent': None},
{'id': 32, 'user_id': 7, 'notification': '{"created": "2023-09-16 05:58", "expiration": "2023-12-29 01:05", "interval": "60", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:AP-FOFB:LoopState-Sts", "rule0": "pv == L", "limit0": "0", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 33, 'user_id': 7, 'notification': '{"created": "2023-09-16 05:59", "expiration": "2023-12-29 20:01", "interval": "30", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:AP-CurrInfo:Current-Mon", "rule0": "pv <= L", "limit0": "99.5", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-InjCtrl:Mode-Sts", "rule1": "pv == L", "limit1": "1", "subrule1": ""}}]}', 'last_sent': None},
{'id': 34, 'user_id': 7, 'notification': '{"created": "2023-09-16 06:01", "expiration": "2023-12-29 05:46", "interval": "60", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-.+:VA-SIP.+Pressure-Mon", "rule0": "pv == L", "limit0": "0", "subrule0": "OR"}}, {"notificationCore1": {"pv1": "SI-.+:VA-SIP.+Pressure-Mon", "rule1": "pv >= L", "limit1": "1e-8", "subrule1": ""}}]}', 'last_sent': None},
{'id': 35, 'user_id': 7, 'notification': '{"created": "2023-09-16 06:02", "expiration": "2023-12-29 03:59", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:DI-BbBProc-L:SAT", "rule0": "pv == L", "limit0": "1", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 36, 'user_id': 2, 'notification': '{"created": "2023-09-16 06:03", "expiration": "2024-12-30 23:59", "interval": "60", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "TS-04:PU-InjSeptG-1:Voltage-Mon", "rule0": "pv < L", "limit0": "812.6", "subrule0": "OR"}}, {"notificationCore1": {"pv1": "TS-04:PU-InjSeptG-2:Voltage-Mon", "rule1": "pv < L", "limit1": "810.8", "subrule1": ""}}]}', 'sms_text': "TS's Septa Problem!", 'last_sent': None},
{'id': 37, 'user_id': 8, 'notification': '{"created": "2023-09-16 06:08", "expiration": "2023-08-26 19:00", "interval": "30", "persistence": "NO", "notificationCores": [{"notificationCore0": {"pv0": "SI-Glob:AP-CurrInfo:Current-Mon", "rule0": "pv < L", "limit0": "99.85", "subrule0": ""}}]}', 'last_sent': None},
{'id': 38, 'user_id': 8, 'notification': '{"created": "2023-09-16 06:07", "expiration": "2023-08-26 19:00", "interval": "30", "persistence": "NO", "notificationCores": [{"notificationCore0": {"pv0": "SI-13C4:DI-DCCT:Current-Mon", "rule0": "pv <= L", "limit0": "99.5", "subrule0": ""}}]}', 'last_sent': None},
{'id': 39, 'user_id': 2, 'notification': '{"created": "2023-09-21 03:03", "expiration": "2023-09-22 02:53", "interval": "60", "persistence": "NO", "notificationCores": [{"notificationCore0": {"pv0": "SI-13C4:DI-DCCT:Current-Mon", "rule0": "(pv < LL) and (pv > LU)", "limitLL0": "0", "limitLU0": "1", "subrule0": ""}}]}', 'last_sent': None},
{'id': 40, 'user_id': 7, 'notification': '{"created": "2023-09-21 04:39", "expiration": "2023-12-29 02:57", "interval": "10", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "TU-.+:AC-PT100:MeanTemperature-Mon", "rule0": "(pv < LL) and (pv > LU)", "limitLL0": "23", "limitLU0": "24", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "0", "subrule1": ""}}]}', 'last_sent': None},
{'id': 41, 'user_id': 2, 'notification': '{"created": "2023-09-22 20:19", "expiration": "2023-09-23 20:18", "interval": "60", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "SI-13C4:DI-DCCT:Current-Mon", "rule0": "(pv > LL) and (pv < LU)", "limitLL0": "99", "limitLU0": "100.5", "subrule0": "AND"}}, {"notificationCore1": {"pv1": "AS-Glob:AP-MachShift:Mode-Sts", "rule1": "pv == L", "limit1": "1", "subrule1": ""}}]}', 'last_sent': None}]

notifications_raw2 = \
[{'id': 36, 'user_id': 2, 'notification': '{"created": "2023-09-16 06:03", "expiration": "2024-12-30 23:59", "interval": "60", "persistence": "YES", "notificationCores": [{"notificationCore0": {"pv0": "TS-04:PU-InjSeptG-1:Voltage-Mon", "rule0": "pv < L", "limit0": "812.6", "subrule0": "OR"}}, {"notificationCore1": {"pv1": "TS-04:PU-InjSeptG-2:Voltage-Mon", "rule1": "pv < L", "limit1": "810.8", "subrule1": ""}}]}', 'sms_text': "TS's Septa Problem!", 'last_sent': None}]
