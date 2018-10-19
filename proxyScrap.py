from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
import traffic
import random
import urllib2
import smtplib

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = []
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[5][contains(text(),"elite proxy")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.append(proxy)
    return proxies


#If you are copy pasting proxy ips, put in the list below

# url = 'https://httpbin.org/ip'

while True:
    proxies = get_proxies()
    # proxy_pool = cycle(proxies)
    w = []
    for i in range(len(proxies)):
        #Get a proxy from the pool
        r = random.randint(0,len(proxies))
        proxy = proxies[r]
        while proxies[r] in w:
          r = random.randint(0,len(proxies))
          proxy = proxies[r]
        w.append(proxies[r])
        print("Request #%d"%i)
        print proxy
        try:
            traffic.traffic(proxy)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except requests.exceptions.ProxyError:
            #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
            #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url         
            print("Skipping. Connnection error")
        except requests.exceptions.ConnectionError:
            continue
        except Exception,e:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login('codeguardian1@gmail.com','traffic_notifier')
            msg1 = "\r\n".join([
              "From: Code Guardian",
              "To: rashna_kumar@ymail.com",
              "Subject: Code Crashed",
              "",
              "Why, oh why"
              ])
            msg2 = "\r\n".join([
              "From: Code Guardian",
              "To: ddar203@gmail.com",
              "Subject: Code Crashed",
              "",
              "\nWhy, oh why"
              ])
            server.sendmail('codeguardian1@gmail.com',"rashna_kumar@ymail.com",msg1)
            server.sendmail('codeguardian1@gmail.com','ddar203@gmail.com',msg2)
            server.quit()
            raise KeyboardInterrupt