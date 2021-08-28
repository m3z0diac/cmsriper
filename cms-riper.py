import requests
import os
import time
from config_file import ConfigFile
import optparse
import socket
from queue import Queue
import threading
import time


config = ConfigFile("apis.ini")
API_KEY = config.get('api_per_line.api_key', parse_types=True)

'''
Hamza Elansari && Salah Ddin HK-GANG
'''

__banner__ = """
       +=======================================+
       |.........CMS RIPER PROJECT v 1 ........|
       +---------------------------------------+
       |#Author: Hamza07-w - salahddin         |
       |#Contact: Instagram @hamza07.py        |
       |          hamzaelansari453@gmail.com   | 
       |#Date: Aug 28  19:20:49 2021           |
       |#This tool is made for pentesting.     |
       |#I take no responsibilities for the    |
       |  use of this program !                |
       +=======================================+
       |.........CMS RIPER PROJECT v 1.........|
       +---------------------------------------+
"""
print(__banner__)

def getArg():
    parser = optparse.OptionParser()
    parser.add_option("-u", "--url", dest="url", help="Website Target Url/ http://example.com")
    (options, arg) = parser.parse_args()
    return options


def getCMSResults(url,verbose=False):

    try:        
        res=requests.get(f"https://whatcms.org/API/Tech?key={API_KEY}&url={url}")
    except requests.exceptions.ConnectionError:
        print("Unable To Connect To the Internet.")
        exit(1)
    if res.status_code==200:
        if res.json()["result"]["code"]==101:
            print("INVALID API KEY!.")
            exit(1)
        if res.json()["result"]["code"]==120:
            tts=float(res.json()["retry_in_seconds"])
            if verbose:
                print(f"Maxium API Request Reached. Trying Again in {tts} seconds.  ")
            time.sleep(tts)
            return getCMSResults(url,verbose)
        if verbose:
            print(res.text)
        cms=None
        infos = res.json()["results"]
        print(f"-------{url} Technologie Informations-------\n")
        try:
            print(f"CMS : {infos[0]['name']} Version {infos[0]['version']}")
            print(f"Programming Lang : {infos[1]['name']}")
            print(f"Databases : {infos[2]['name']}")
            print(f"Web Server : {infos[3]['name']}")
        except:
            print(f"CMS : {infos[1]['name']} Version {infos[1]['version']}")
            print(f"Programming Lang : {infos[2]['name']}")
            print(f"Databases : {infos[3]['name']}")
            print(f"Web Server : {infos[4]['name']}")

        if len(res.json()["meta"]) >0:
            sinfos = res.json()["meta"]["social"]
            print(f"\n-------{url} Social Media Informations-------\n")
            for i in range(len(sinfos)):
                print(f"{sinfos[i]['network']} ==> {sinfos[i]['url']}")



options = getArg()
input_file = options.url
queue =Queue()
open_ports = []


def scan(port):
    '''
    creat a socket and try to make connection with target ip
    '''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((options.url, port))
        return True

    except:
        return False

def fill_queque(port_list):
    '''
    fill the queue, (put all ports in stack)
    '''
    for port in port_list:
        queue.put(port)

def worker():
    '''
    scan an IP or a Host for get all open ports
    '''
    while not queue.empty():
        port = queue.get()
        if scan(port):
            service = socket.getservbyport(port)

            print(f"[+] port {port} is open! ---service {service}")
            open_ports.append(port)

def final_port_scan():
    print(f"\n-------{options.url} Ports Scanning-------\n")
    port_list = range(1, 1024)
    fill_queque(port_list)

    thread_list = []

    for t in range(50):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("open ports are: ", open_ports)

getCMSResults(input_file)
s = input(f"\nDo you wanna scann {input_file} Ports(y/n)? ")
if s == 'y':
    final_port_scan()
else:
    print("cancel port scanning and exit!")