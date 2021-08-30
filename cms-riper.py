import requests
import os
from config_file import ConfigFile
import optparse
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

getCMSResults(input_file)
