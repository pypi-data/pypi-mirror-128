# -*- coding: utf-8 -*-
# pylint: disable=line-too-long


from random import randint
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


def getBrowserType(rnd=0):
    browser = []
    dSet=getDataSet()
    unique = [x for x in dSet if x['browser'] not in browser and (browser.append(x['browser']) or True)]

    if rnd != 0:
        i=randint(0,len(browser)-1)
        browser=[browser[i]]

    return browser


def getUserAgent(so=None, browser=None, hardwareType=None):
    if (so==None):
        so=getSO(1)

    if (browser==None):
        browser=getBrowserType(1)

    if (hardwareType==None):
        hardwareType=getHardwareType(1)

    items = []
    dSet=getDataSet()
    unique = [x for x in dSet if (x['browser']==browser) and (x['so']==so) and (x['hardwareType']==hardwareType) and (items.append(x) or True)]
    
    #random items
    i=randint(0,len(items)-1)
    items=[items[i]]
    return items



def script_ua():
    print('Ciao')
    
def generate_navigator(i):
    print (i)
    return (i+1)
