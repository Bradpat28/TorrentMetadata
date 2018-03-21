import os
import pickle
import sys
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np


from torrentClass import TorrentInfoClass
from torrentClass import TrackerInfoClass
from torrentClass import PeerInfoClass










def main():
    fileToLookFor = None

    if len(sys.argv) > 1:
        fileToLookFor = sys.argv[1]


    os.chdir("data")
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
                    lat = float(peer.loc.split(",")[0])
                    lon = float(peer.loc.split(",")[1])
                    coordData.append((lon,lat))
            #tClass.printSelf()
        elif torrentData == fileToLookFor:
            tClass = pickle.load(open(torrentData, "r" ))

    # plot coastlines, draw label meridians and parallels
    # Map (long, lat) to (x, y) for plotting
    for cord in coordData:
        print "longitude - " + str(cord[0]) + " Latitude - " + str(cord[1])
        x, y = map(cord[0], cord[1])
        plt.plot(x, y, 'ok', markersize=2)

    plt.show()






if __name__ == '__main__':
    main()
