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