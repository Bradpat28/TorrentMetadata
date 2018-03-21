import os
import pickle
import sys
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import operator
import pandas



from torrentClass import TorrentInfoClass
from torrentClass import TrackerInfoClass
from torrentClass import PeerInfoClass


MY_IP_ADDR = "0.0.0.0"


def getMapFromClasses(fileToLookFor):
    map = Basemap(projection='cyl', resolution=None,
            llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=-180, urcrnrlon=180, )
    map.etopo(scale=0.5, alpha=0.5)
    coordData = []
    for torrentData in os.listdir("."):
        if fileToLookFor == None:
            tClass = pickle.load(open(torrentData, "r" ))
            for tracker in tClass.trackerList:
                for peer in tracker.peers:
                    if peer.ip != MY_IP_ADDR:
                        lat = float(peer.loc.split(",")[0])
                        lon = float(peer.loc.split(",")[1])
                        if coordData.count((lon,lat)) == 0:
                            coordData.append((lon,lat))
            #tClass.printSelf()
        elif torrentData == fileToLookFor:
            tClass = pickle.load(open(torrentData, "r" ))

    # plot coastlines, draw label meridians and parallels
    # Map (long, lat) to (x, y) for plotting
    for cord in coordData:
        #print "longitude - " + str(cord[0]) + " Latitude - " + str(cord[1])
        x, y = map(cord[0], cord[1])
        plt.plot(x, y, 'ok', markersize=2)

    plt.show()


def getDataFromClasses():

    countryList = {}
    orgList = {}
    ipAddress = {}
    #num peers torrent has

    for torrentData in os.listdir("."):
        tClass = pickle.load(open(torrentData, "r" ))
        for tracker in tClass.trackerList:
            for peer in tracker.peers:
                if peer.ip != MY_IP_ADDR:
                    if not (peer.country in countryList):
                        countryList[peer.country] = 1
                    else:
                        countryList[peer.country] += 1

                    if not (peer.org in orgList):
                        orgList[peer.org] = 1
                    else:
                        if peer.org != "":
                            orgList[peer.org] += 1

                    if not (peer.ip in ipAddress):
                        ipAddress[peer.ip] = 1
                    else:
                        ipAddress[peer.ip] += 1

    print "---------------------Country Lists--------------"
    sortCountry = sorted(countryList.items(), key=operator.itemgetter(1), reverse=True)
    sortOrg = sorted(orgList.items(), key=operator.itemgetter(1), reverse=True)
    sortIp = sorted(ipAddress.items(), key=operator.itemgetter(1), reverse=True)

    df = pandas.DataFrame(sortCountry[0:50], columns=['country', 'frequency'])
    df.plot(kind='bar', x='country')

    df = pandas.DataFrame(sortOrg[0:50], columns=['org', 'frequency'])
    df.plot(kind='bar', x='org')

    df = pandas.DataFrame(sortIp[0:50], columns=['ip', 'frequency'])
    df.plot(kind='bar', x='ip')

    for x,value in sortCountry:
        #xCord.append(x)
        #yCord.append(value)
        print x + " has " + str(value)

    for x,value in sortOrg:
        if value > 5:
            print x + " has " + str(value)

    for x,value in sortIp:
        if value > 2:
            print x + " has " + str(value)
    plt.show()




def main():
    fileToLookFor = None

    if len(sys.argv) > 1:
        fileToLookFor = sys.argv[1]
    os.chdir("data")
    getDataFromClasses()
    getMapFromClasses(fileToLookFor)







if __name__ == '__main__':
    main()
