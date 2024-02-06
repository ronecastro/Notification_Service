#!./venv/bin/python
from db import App_db, FullPVList
from utils import makepvlist, connect_pvs
from epics import PV

def evaluate():
    f = FullPVList()
    f.update()
    fullpvlist = f.getlist()
    while True:
        try:
            # allpvs = makepvlist(fullpvlist)
            allpvs = ['SI-13C4:DI-DCCT:Current-Mon', 'RAD:Thermo3:TotalDoseRate:Dose', 'AS-Glob:AP-MachShift:Mode-Sts', 'TU-0160:AC-PT100:MeanTemperature-Mon', 'SI-03B2FE:VA-SIP150-MD:Pressure-Mon']
            pvlist = connect_pvs(allpvs)
            for pv in pvlist:
                if pv.connected:
                    print(pv.pvname, pv.value)
                else:
                    print(pv.pvname, 'NOT CONNECTED')
        except KeyboardInterrupt:
            break


evaluate()
