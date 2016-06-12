import googlemaps
import sqlite3
import os
from datetime import datetime

def getAPIKey():
    path = "google-api-key.txt"
    if (os.path.exists(path)):
        f = open(path, 'r')
        result = f.read()
        f.close()
        return result.strip()

def getDirections(source, destination):
    badInput = False

    sPl = gmaps.places(source)
    if (str(sPl[u'status']) == "ZERO_RESULTS"):
        print "Bad Source"
        badInput = True
    else:
        src = str(sPl[u'results'][0][u'formatted_address'])
        sID = str(sPl[u'results'][0][u'place_id'])

    dPl = gmaps.places(destination)
    if (str(dPl[u'status']) == "ZERO_RESULTS"):
        print "Bad Destination"
        badInput = True
    else:
        dst = str(dPl[u'results'][0][u'formatted_address'])
        dID = str(dPl[u'results'][0][u'place_id'])

    if badInput:
        return (None, None)

    dirs = gmaps.directions(src, dst, departure_time=datetime.now())
    dirsInfo = dirs[0][u'legs'][0]

    time = dirsInfo[u'duration_in_traffic'][u'value']
    dist = dirsInfo[u'distance'][u'value']

    if (time < 60):
        tNew = str(time) + " seconds"
    elif (time < 60 * 60):
        tNew = str(round(time / 60.0, 2)) + " minutes"
    elif (time < 60 * 60 * 24):
        tNew = str(round(time / 60.0 / 60.0, 2)) + " hours"
    else:
        tNew = str(round(time / 60.0 / 60.0 / 24.0, 2)) + " days"

    dNew = str(round(0.000621371 * dist, 2)) + " miles"

    print "Source: " + src
    print "Destination: " + dst
    print "t = " + tNew
    print "d = " + dNew

    return (sID, dID)

# Unique Google API Key
gmaps = googlemaps.Client(key=getAPIKey())

def main():
    sIn = raw_input("Enter source: ")
    dIn = raw_input("Enter destination: ")
    (srcID, dstID) = getDirections(sIn, dIn)

if __name__ == "__main__":
    main()
