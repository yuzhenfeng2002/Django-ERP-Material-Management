def getRegex(string):
    if string == '':
        return r'.*'
    else:
        return string

def getPk(string):
    if string == '':
        return r'.*'
    else:
        return str(int(string))