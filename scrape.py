from tpb import TPB
from tpb import CATEGORIES, ORDERS
import os
import glob
import re
import subprocess
from threading import Timer




def main():
    t = TPB('https://thepiratebay.org')
    createTorrentDirectory()
    movieFile = open("movieList.txt", "r")
    totRes = 0
    totMovies = 0
    for line in movieFile.readlines():
        print "MOVIE - " + line.split("\n")[0]
        search = t.search(line.split("\n")[0])
        for torrent in search:
            saveTorrentInDir("./Torrents", torrent)
            print "\t" + torrent.title
            totRes += 1
        totMovies += 1

    print "Total Movies = " + str(totMovies)
    print "TotalRes = " + str(totRes)


def saveTorrentInDir(dirName, torrentMetadata):
    x = 20
    delay = 1.0
    my_timeout = int(x / delay)
    convString = "python Magnet_To_Torrent2.py -m \"" + \
        torrentMetadata.magnet_link + "\" -o " + \
        dirName + "/" + re.sub('[!@#$ ()]', '', torrentMetadata.title) + ".torrent"
    print convString
    p = subprocess.Popen(convString, shell=True)
    timer1 = Timer(my_timeout, p.kill)
    timer1.start()
    p.communicate()
    if timer1.is_alive():
        timer1.cancel()
        return
    print("TIMEDOUT THE PROCESS")


def createTorrentDirectory():
    #Make a Directory to store the torrents
    torDir = glob.glob("./Torrents")
    if len(torDir) == 0:
        os.mkdir("./Torrents")



if __name__ == '__main__':
    main()
