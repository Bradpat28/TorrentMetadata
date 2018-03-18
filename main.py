from tpb import TPB
from tpb import CATEGORIES, ORDERS

t = TPB('https://thepiratebay.org')

search = t.search('Stranger Things', category=CATEGORIES.VIDEO.TV_SHOWS)

numberOfResults = 0

for torrent in search:
    #print (torrent.info)
    torrent.print_torrent()
    numberOfResults += 1

print(numberOfResults)
