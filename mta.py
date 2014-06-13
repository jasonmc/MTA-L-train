import gtfs_realtime_pb2
import urllib2
from datetime import datetime

url = "http://datamine.mta.info/files/k38dkwh992dk/gtfs-l"


def getFeedMessage():
    fm = gtfs_realtime_pb2.FeedMessage()
    response = urllib2.urlopen(url)
    data = response.read()
    fm.ParseFromString(data)
    return fm


def getTrain(feedMessage, i):
    return list((x.stop_id, datetime.datetime.fromtimestamp(x.departure.time))
                for x in feedMessage.entity[i].trip_update.stop_time_update)


def timesForStop(feedMessage, stopId):
    return (datetime.fromtimestamp(y.departure.time)
            for x in feedMessage.entity
            for y in x.trip_update.stop_time_update
            if y.stop_id == stopId)


def getMinsUntil(departTime):
    # acceptable to err on the side of caution and round down
    return (departTime - datetime.now()).seconds / 60


def formatIt(departTime, mins):
    return (departTime.strftime("%I:%M %p") + " : " + str(mins) + " mins")


def main():
    jefferson = "L15N"
    times = timesForStop(getFeedMessage(), jefferson)
    for x in(formatIt(x, getMinsUntil(x)) for x in times):
        print x

if __name__ == '__main__':
    main()
