# -*- coding: utf-8 -*-
# pylint: disable=line-too-long


from random import choice, randint
from datetime import datetime, timedelta




def getSO(rnd=0):
    so = []
    dSet=getDataSet()

    unique = [x for x in dSet if x['so'] not in so and (so.append(x['so']) or True)]

    if rnd != 0:
        i=randint(0,len(so)-1)
        so=[so[i]]

    return so


def getHardwareType(rnd=0):
    hw = []
    dSet=getDataSet()
    unique = [x for x in dSet if x['hardwareType'] not in hw and (hw.append(x['hardwareType']) or True)]

    if rnd != 0:
        i=randint(0,len(hw)-1)
        hw=[hw[i]]

    return hw




def script_ua():
    print('Ciao')
    
def generate_navigator(i):
    print (i)
    return (i+1)
