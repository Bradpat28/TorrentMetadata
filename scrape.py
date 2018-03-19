from tpb import TPB
from tpb import CATEGORIES, ORDERS
import os
import glob




def main():
    t = TPB('https://thepiratebay.org')

    search = t.search('Stranger Things', category=CATEGORIES.VIDEO.TV_SHOWS)

    numberOfResults = 0

    createTorrentDirectory()

    for torrent in search:
        saveTorrentInDir("./Torrents", torrent)
        #torrent.print_torrent()
        numberOfResults += 1

    print(numberOfResults)


def saveTorrentInDir(dirName, torrentMetadata):
    convString = "python Magnet_To_Torrent2.py -m \"" + \
        torrentMetadata.magnet_link + "\" -o " + \
        dirName + "/" + torrentMetadata.title + ".torrent"
    print convString
    os.system(convString)


def createTorrentDirectory():
    #Make a Directory to store the torrents
    torDir = glob.glob("./Torrents")
    if len(torDir) == 0:
        os.mkdir("./Torrents")



if __name__ == '__main__':
    main()
