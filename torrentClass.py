

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
    def __init__(self, hostName, jsonData):
        self.hostName = hostName
        self.jsonData = jsonData

    def printSelf(self):
        print "\thostname = " + self.hostName
