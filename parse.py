import torrent_parser as tp
import os
import sys
import requests
import socket
import pprint
import json
import time
import libtorrent as lt
import glob
import pickle
import shutil
from torrentClass import TorrentInfoClass
from torrentClass import TrackerInfoClass
from torrentClass import PeerInfoClass
from threading import Timer


#define a global pretty printer
PP = pprint.PrettyPrinter(indent=4)

def ip_to_location(ip_addr):
    print 'http://ipinfo.io/' + ip_addr + "/json"
    ip_loc = requests.get('http://ipinfo.io/' + ip_addr + "/json?token=63b3970ce0077f").json()
    #NOT WORKING ON MY MACHINE!
    """
    data = {'ip': '8.8.8.8',
          "hostname": 'google-public-dns-a.google.com',
          'loc': '37.385999999999996,-122.0838',
          'org': "AS15169 Google Inc.",
          'city': 'Mountain View',
          'region': 'California',
          'country': 'US',
          'phone': 650}
    json_data = json.dumps(data)
    """
    #return json_data
    return ip_loc#json_data

def dns_resolve(hostname):
    try:
        return socket.gethostbyname(hostname)
    except:
        #print "Could not resolve Host:" + hostname
        return None


def analyze_data(torrent_data, torrentName):
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
                    tInfo = TrackerInfoClass(str, loc, getPeerData(torrentName))
                    trackObjList.append(tInfo)
            #print tracker_list
    return trackObjList

def getPeerData(torrentFileName):
    peerList = []
    ses = lt.session()
    ses.listen_on(6881, 6891)
    info = lt.torrent_info(torrentFileName)
    tempDir = glob.glob("./temp")
    if len(tempDir) == 0:
        os.mkdir("./temp")
    h = ses.add_torrent({'ti': info, 'save_path': './temp'})

    print 'starting', h.name()

    timeCount = 0
    timeout = False
    ipList = []

    while (not h.is_seed()) and (timeout != True):
        s = h.status()
        p = h.get_peer_info()
        for peer in p:
            #print peer.ip
            if ipList.count(peer.ip[0]) == 0:
                search_ip = str(peer.ip).split("'")[1]
                jsonData = ip_to_location(search_ip)
                if jsonData != None:
                    print jsonData
                    print "Saved Data"
                    peerClass = PeerInfoClass()
                    info = jsonData#json.loads(jsonData)
                    peerClass.jsonData = jsonData
                    peerClass.loc = info['loc']
                    peerClass.country = info['country']
                    peerClass.org = info['org']
                    peerClass.ip = search_ip
                    peerClass.region = info['region']
                    #peerClass.hostname = info['hostname']
                    peerClass.city = info['city']
                    peerList.append(peerClass)
                    ipList.append(peer.ip[0])
        sys.stdout.flush()
        timeCount += 1
        if timeCount > 20:
            timeout = True
        time.sleep(1)

    print h.name(), 'complete'

    shutil.rmtree("./temp")
    return peerList


def main():
    os.chdir("Torrents")
    torrentClassList = []
    for torrent in os.listdir("."):
        print("Getting Metadata for torrent file: " + torrent)
        try:
            data = tp.parse_torrent_file(torrent)
            torrentClassList.append(TorrentInfoClass(torrent, analyze_data(data, torrent)))
        except:
            print "Bad Torrent File " + torrent

    os.chdir("..")
    tempDir = glob.glob("./data")
    if len(tempDir) == 0:
        os.mkdir("./data")
    os.chdir("./data")

    for x in torrentClassList:
        x.printSelf()


        with open(x.className + "Data", "w") as f:
            pickle.dump(x, f)



if __name__ == "__main__":
    main()
