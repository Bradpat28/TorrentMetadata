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
    map = Basemap(projection='mill',lon_0=180)
    for torrentData in os.listdir("."):
        if fileToLookFor == None:
            tClass = pickle.load(open(torrentData, "r" ))
            for tracker in tClass.trackerList:
                for peer in tracker.peers:
                    x = float(peer.loc.split(",")[0])
                    y = float(peer.loc.split(",")[1])
                    map.scatter(x,y)


            #tClass.printSelf()
        elif torrentData == fileToLookFor:
            tClass = pickle.load(open(torrentData, "r" ))
    # plot coastlines, draw label meridians and parallels.
    map.drawcoastlines()
    map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
    map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])
    # fill continents 'coral' (with zorder=0), color wet areas 'aqua'
    map.drawmapboundary(fill_color='aqua')
    map.fillcontinents(color='white',lake_color='aqua')
    # shade the night areas, with alpha transparency so the
    # map shows through. Use current time in UTC.
    map.scatter(75,75)
    plt.title('Peer ip Locations')
    plt.show()





if __name__ == '__main__':
    main()
