import pprint
import os
import requests
import socket
import libtorrent as lt
import time
import sys
import hashlib

#define a global pretty printer
PP = pprint.PrettyPrinter(indent=4)
#define global for different states of download
STATE_STR = ['queued', 'checking', 'downloading metadata', \
             'downloading', 'finished', 'seeding', 'allocating', 'other']


def print_torrent_progress(curr_stat):
        print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %2d) %s\r' % \
                (curr_stat.progress * 100, curr_stat.download_rate / 1000, curr_stat.upload_rate / 1000, \
                curr_stat.num_peers, STATE_STR[curr_stat.state]),
        sys.stdout.flush()

def ip_to_location(ip_addr):
    ip_loc = requests.get('http://ipinfo.io/' + ip_addr).json()
    print ip_loc

def dns_resolve(hostname):
    try:
        ip_addr = socket.gethostbyname(hostname)
        print hostname + " is at " + ip_addr
    except:
        print "DNS QUERY FOR " + hostname + " FAILED!"

def get_hash_and_compare(piece_num, torrent_info):

    hash_str = torrent_info.hash_for_piece(piece_num)
    print "Hash for piece " + str(piece_num) + " is: " + str(hash_str)


def process_alerts(alert_list, torrent_info):
    if alert_list is not None:
        for alert in alert_list:
            if isinstance(alert, lt.piece_finished_alert):
                piece_num = alert.__str__().split(":")[-1]
                piece_num = int(''.join(c for c in
                    piece_num if c.isdigit()))
                get_hash_and_compare(piece_num, torrent_info)

def process_current_peers(peer_info):
    for peer in peer_info:
        print peer.ip
        search_ip = str(peer.ip).split("'")[1]
        ip_to_location(search_ip)

def get_torrent_block(torrent_name):

    ses = lt.session()
    ses.listen_on(6881, 6891)

    e = lt.bdecode(open(torrent_name, 'rb').read())
    info = lt.torrent_info(e)

    #for tracker in info.trackers():
    #    url = tracker.url
    #    url = url.replace("/", "")
    #    url = url.split(":")[1]
    #    dns_resolve(url)
    

    params = {
        'save_path': '../Completed/' + torrent_name.split(".torrent")[0],
        'storage_mode': lt.storage_mode_t(2),
        'paused': False,
        'auto_managed': False,
        'duplicate_is_error': True,
        'ti': info
    }
    
    handle = ses.add_torrent(params)
    #make sure we get the alerts for when a piece finished
    ses.set_alert_mask(lt.alert.category_t.progress_notification)

    #needs to be set 
    stat = handle.status()
    while (not stat.is_seeding):
        #update status
        stat = handle.status()
        
        #get all current peer info
        peer_info = handle.get_peer_info()
        process_current_peers(peer_info)

        #wait for an alert --- timeout might be hit for slow torrent
        #ses.wait_for_alert(500)
        #alert_list = ses.pop_alerts()
        #process_alerts(alert_list, info)
        

        print_torrent_progress(stat)
        time.sleep(1)
   
    #finally, remove the torrent once starting to seed
    ses.remove_torrent(handle)


def main():
    os.chdir("Torrents")
    for torrent in os.listdir("."):
        if torrent.endswith(".torrent"):
            print("Checking pieces for torrent file: " + torrent)
            get_torrent_block(torrent)

if __name__ == "__main__":
    main()
