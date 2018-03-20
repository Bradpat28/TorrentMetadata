

class TorrentInfoClass:
    def __init__(self, className, trackerList):
        self.className = className
        self.trackerList = trackerList

    def printSelf(self):
        print "----------------------"
        print "Torrent Class - " + self.className
        for x in self.trackerList:
            x.printSelf()




class TrackerInfoClass:
    def __init__(self, hostName, jsonData, peers):
        self.hostName = hostName
        self.jsonData = jsonData
        self.peers = peers

    def printSelf(self):
        print "\thostname = " + self.hostName
        for x in peers:
            x.printSelf()



class PeerInfoClass:
    def __init__(self, jsonData):
        self.jsonData = jsonData

    def printSelf(self):
        for key,value in self.jsonData.iteritems():
            print key
            print value
