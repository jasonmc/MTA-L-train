import txt_pb2
import gtfs_realtime_pb2
import urllib2
from datetime import datetime

url = "http://datamine.mta.info/files/k38dkwh992dk/gtfs-l"


def getData():
    response = urllib2.urlopen(url)
    data = response.read()
    o2.ParseFromString(data)


obj = txt_pb2.NyctFeedHeader()


o2 = gtfs_realtime_pb2.FeedMessage()


getData()


def getTrain(i):
    return list((x.stop_id, datetime.datetime.fromtimestamp(x.departure.time))
                for x in o2.entity[i].trip_update.stop_time_update)


def timesForStop(stopId):
    thisStopTimes = (y for x in o2.entity
                     for y in x.trip_update.stop_time_update
                     if y.stop_id == stopId)
    for j in thisStopTimes:
        departTime = datetime.fromtimestamp(j.departure.time)

        # acceptable to err on the side of caution and round down
        mins = (departTime - datetime.now()).seconds / 60

        print departTime.strftime("%I:%M %p"), ":", mins, "mins"


def main():
    jefferson = "L15N"

    timesForStop(jefferson)

main()
