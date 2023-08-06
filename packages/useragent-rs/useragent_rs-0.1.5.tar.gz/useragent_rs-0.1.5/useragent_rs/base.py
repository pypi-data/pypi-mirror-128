# -*- coding: utf-8 -*-
# pylint: disable=line-too-long


from random import randint
from datetime import datetime, timedelta
from useragent_rs.dataset import *

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

def getUserAgent():
    dSet=getDataSet()
    i=randint(0,len(dSet)-1)
    dSet=[dSet[i]]
    return dSet

def getUserAgentForSO(so=None):
    if (so==None):
        so=getSO(1)

    items = []
    dSet=getDataSet()
    unique = [x for x in dSet if   (x['so'] in so) and (items.append(x) or True)]
    
    if (len(items)>0):
        #random items
        i=randint(0,len(items)-1)
        items=[items[i]]
    else:
        items=[]

    return items

def getUserAgentForBrowser(browser=None):
    if (browser==None):
        browser=getBrowserType(1)

    items = []
    dSet=getDataSet()
    unique = [x for x in dSet if (x['browser'] in browser)  and (items.append(x) or True)]
    
    if (len(items)>0):
        #random items
        i=randint(0,len(items)-1)
        items=[items[i]]
    else:
        items=[]

    return items

def getUserAgentForHW(hw=None):
    if (hw==None):
        hw=getHardwareType(1)

    items = []
    dSet=getDataSet()
    unique = [x for x in dSet if (x['hardwareType'] in hw)  and (items.append(x) or True)]
    
    if len(items)>0:
        #random items
        i=randint(0,len(items)-1)
        items=[items[i]]
    else:
        item=[]

    return items


def script_ua():
    return getUserAgent()
    

