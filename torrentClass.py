

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
        for x in self.peers:
            x.printSelf()



class PeerInfoClass:
    def __init__(self):
        self.jsonData = None
        self.ip = ""
        self.loc = ""
        self.country = ""
        self.org = ""
        self.city = ""
        self.hostname = ""
        self.region = ""


    def printSelf(self):
        #print self.jsonData
        print "\t\t----------------------"
        print "\t\tIP addr - " + self.ip
        print "\t\tCountry - " + self.country
        print "\t\tloc - " + self.loc
        print "\t\torg - " + self.org
        print "\t\tcity - " + self.city
        print "\t\tregion - " + self.region
        print "\t\thostname - " + self.hostname
