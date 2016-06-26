#!/usr/bin/env python

import re, xml.etree.ElementTree as ET
from sys import version_info

if version_info >= (3, 0):
    import urllib.request as urllib
else:
    import urllib2 as urllib

__version__ = "1.0"

def getExternalIP():
    regex = ('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' * 4)[:-2]
    ip = re.search(regex, httpGET('http://checkip.dyndns.org/plain')).group(0)
    return ip if len(ip) > 0 else ''

def httpGET(url):
    result = urllib.urlopen(url)
    content = result.read()
    result.close
    return content

def buildUpdateURL(host, domain, password, ip):
    args = {'host': host, 'domain': domain, 'password': password, 'ip': ip}
    return buildCommandURL(args, 'https://dynamicdns.park-your-domain.com/update?')
    
def buildCommandURL(args, url = 'https://api.namecheap.com/xml.response?'):
    return url + ''.join([(name + '=' + value + '&') for name, value in args.items()])[:-1]

def getConfig():
    root = ET.parse('config.xml').getroot()
    config = {}
    config['ApiUser']  = root.find('ApiUser').text
    config['ApiKey']   = root.find('ApiKey').text
    config['UserName'] = root.find('UserName').text
    config['ClientIp'] = getExternalIP()
    return config

# uses the namecheap.com api
def getDomains_api(config):
    args = dict(config)
    args['Command'] = 'namecheap.domains.getList'
    url = buildCommandURL(args)
    response = httpGET(buildCommandURL(args))
    root = ET.fromstring(response)
    ns = root.tag[:root.tag.find('}') + 1]
    return [domain.get('Name') for domain in root.iter(ns + 'Domain')]

# uses the namecheap.com api
def getHostnames_api(config, domain):
    args = dict(config)
    args['Command'] = 'namecheap.domains.dns.getHosts'
    args['SLD'], args['TLD'] = domain.split('.')
    response = httpGET(buildCommandURL(args))
    print response
    root = ET.fromstring(response)
    ns = root.tag[:root.tag.find('}') + 1]
    return [host.get('Name') for host in root.iter(ns + 'Host')]

def getDomains():
    root = ET.parse('domains.xml').getroot()
    return {domain.get('name'): domain.get('password') for domain in root.findall('Domain')}

def getHostnames(domain):
    root = ET.parse('domains.xml').getroot()
    for d in root.findall('Domain'):
        if d.get('name') == domain:
            return [host.get('name') for host in d.iter('Host')]

def updateDomains():
    config = getConfig()
    ip = getExternalIP()
    for domain, password in getDomains().items():
        updateURLs = [buildUpdateURL(host, domain, password, ip) for host in getHostnames(domain)]
        print [httpGET(url) for url in updateURLs]

updateDomains()
