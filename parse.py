import torrent_parser as tp
import os
import requests
import socket
import pprint
import json
from torrentClass import TorrentInfoClass
from torrentClass import TrackerInfoClass

#define a global pretty printer
PP = pprint.PrettyPrinter(indent=4)

def ip_to_location(ip_addr):
    print 'http://ipinfo.io/' + ip_addr + "/json"
    ip_loc = requests.get('http://ipinfo.io/' + ip_addr + "/json").json()
    return ip_loc

def dns_resolve(hostname):
    try:
        return socket.gethostbyname(hostname)
    except:
        #print "Could not resolve Host:" + hostname
        return None


def analyze_data(torrent_data):
    trackObjList = []
    for key,value in torrent_data.iteritems():
        #if key == "announce":
            #print key, value
        if key == "announce-list":
            tracker_list = list(value[0])
            for tracker in value[0]:
                #print tracker
                str = tracker.split(":")[0] + ":" + tracker.split(":")[1]
                ip = dns_resolve(str)
                if ip != None:
                    loc = ip_to_location(ip)
                    #print loc
                    tInfo = TrackerInfoClass(str, loc)
                    trackObjList.append(tInfo)

            #print tracker_list
    return trackObjList


def main():
    os.chdir("Torrents")
    torrentClassList = []
    for torrent in os.listdir("."):
        print("Getting Metadata for torrent file: " + torrent)
        try:
            data = tp.parse_torrent_file(torrent)
        except:
            print "Bad Torrent File " + torrent
        torrentClassList.append(TorrentInfoClass(torrent, analyze_data(data)))
    for x in torrentClassList:
        x.printSelf()



if __name__ == "__main__":
    main()
