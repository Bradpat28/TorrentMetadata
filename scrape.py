from tpb import TPB
from tpb import CATEGORIES, ORDERS
import os
import glob




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
            #saveTorrentInDir("./Torrents", torrent)
            print "\t" + torrent.title
            totRes += 1
        totMovies += 1

    print "Total Movies = " + str(totMovies)
    print "TotalRes = " + str(totRes)

def saveTorrentInDir(dirName, torrentMetadata):
    convString = "python Magnet_To_Torrent2.py -m \"" + \
        torrentMetadata.magnet_link + "\" -o " + \
        dirName + "/" + torrentMetadata.title + ".torrent"
    os.system(convString)


def createTorrentDirectory():
    #Make a Directory to store the torrents
    torDir = glob.glob("./Torrents")
    if len(torDir) == 0:
        os.mkdir("./Torrents")



if __name__ == '__main__':
    main()
