import datetime
import pytz

def getRegex(string):
    if string == '' or string is None:
        return r'.*'
    else:
        return string

def getPk(string, type='*'):
    if string == '' or string is None:
        return r'.*'
    else:
        return str(int(string))

def getPkExact(string, type='*'):
    if string == '' or string is None:
        return ''
    else:
        return str(int(string))

def getDate(string):
    dateInfo = string.split('. ')
    string = datetime.date(
        year=int(dateInfo[2]), month=int(dateInfo[1]), day=int(dateInfo[0])
    )
    return string


def getDate2(string):
    dateInfo = string.split('. ')
    string = datetime.date(
        year=int(dateInfo[2]), month=int(dateInfo[1]), day=int(dateInfo[0])
    )
    return string