import torrent_parser as tp
import os
import requests
import socket
import pprint

#define a global pretty printer
PP = pprint.PrettyPrinter(indent=4)

def ip_to_location(ip_addr):
    ip_loc = requests.get('http://ipinfo.io/' + ip_addr).json()

def dns_resolve(hostname):
    return socket.gethostbyname(hostname)

def analyze_data(torrent_data):
    for key,value in torrent_data.iteritems():
        if key == "announce":
            print key, value
        if key == "announce-list":
            tracker_list = list(value[0])
            print tracker_list
        if key == "info":

def main():
    os.chdir("Torrents")
    for torrent in os.listdir("."):
        print("Getting Metadata for torrent file: " + torrent)
        data = tp.parse_torrent_file(torrent)
        analyze_data(data)

if __name__ == "__main__":
    main()
