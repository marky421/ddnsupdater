#!/usr/bin/env python

import re, xml.etree.ElementTree as ET
from sys import version_info

PY3K = version_info >= (3, 0)
if PY3K:
    import urllib.request as urllib
else:
    import urllib2 as urllib

__version__ = "1.0"

def getExternalIP():
    regex = '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    ip = re.search(regex, httpGET('http://checkip.dyndns.org/plain')).group(0)
    return ip if len(ip) > 0 else ''

def httpGET(url):
    result = urllib.urlopen(url)
    content = result.read()
    result.close
    return content

def buildURL(host, domain, password, ip):
    return 'https://dynamicdns.park-your-domain.com/update?host=' + host + '&domain=' + domain + '&password=' + password + '&ip=' + ip


def getConfig():
    root = ET.parse('config.xml').getroot()
    config = {}
    config['apiUser']  = root.find('APIUser').text
    config['apiKey']   = root.find('APIKey').text
    config['userName'] = root.find('UserName').text
    return config

print getConfig()
