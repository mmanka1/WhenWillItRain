import json
from datetime import datetime

import PelmorexController


def nextPrecipToString(location):
    locationCode = getLocationCode(location)

    if isinstance(locationCode, int):
        if locationCode == 204:
            return "No location found."
        else:
            return "An error occurred finding a location: HTTP status code %d." % locationCode

    precipStartStop = PelmorexController.getShortTerm(locationCode)
    precipCurrent = PelmorexController.getPrecipStartStop(locationCode)

    if isinstance(precipStartStop, int) or isinstance(precipCurrent, int):
        return "An error occurred getting precipitation data: HTTP status code %d." % precipStartStop

    start = -1
    end = -1

    i = 0

    while i < 32:
        if float(precipStartStop["data"][i]["rain"]) != 0:
            print("If #1: %d" % i)
            start = i
            j = i
            while j < 32:
                if float(precipStartStop["data"][j]["rain"]) == 0:
                    print("If #2: %d" % j)
                    end = j
                    break
                j += 1
        i += 1

    isCurrentPrecipitation = True

    eventsArray = precipCurrent["data"]["events"]
    eventsArrayStr = json.dumps(eventsArray)
    if "[]" in eventsArrayStr:
        isCurrentPrecipitation = False

    print(start)
    print(end)
    print(isCurrentPrecipitation)


def getLocationCode(location):
    locationData = PelmorexController.getLocationData(location)

    if isinstance(locationData, int):
        return locationData

    return locationData["dataCode"]


nextPrecipToString("death%20valley")
