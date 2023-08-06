# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""
This module is for generating random, valid web navigator's
    configs & User-Agent HTTP headers.

Functions:
* generate_user_agent: generates User-Agent HTTP header
* generate_navigator:  generates web navigator's config
* generate_navigator_js:  generates web navigator's config with keys
    identical keys used in navigator object

FIXME:
* add Edge, Safari and Opera support
* add random config i.e. windows is more common than linux

Specs:
* https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent/Firefox
* http://msdn.microsoft.com/en-us/library/ms537503(VS.85).aspx
* https://developer.chrome.com/multidevice/user-agent
* http://www.javascriptkit.com/javatutors/navigator.shtml

Release history:
* https://en.wikipedia.org/wiki/Firefox_release_history
* https://en.wikipedia.org/wiki/Google_Chrome_release_history
* https://en.wikipedia.org/wiki/Internet_Explorer_version_history
* https://en.wikipedia.org/wiki/Android_version_history

Lists of user agents:
* http://www.useragentstring.com/
* http://www.user-agents.org/
* http://www.webapps-online.com/online-tools/user-agent-strings

"""
# pylint: enable=line-too-long

from random import choice, randint
from datetime import datetime, timedelta
import six


def script_ua():
    print('Ciao')
    
def generate_navigator(i):
    print (i)
    return (i+1)
