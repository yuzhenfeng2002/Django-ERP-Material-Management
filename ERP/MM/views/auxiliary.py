def getRegex(string):
    if string == '':
        return r'.*'
    else:
        return string

def getPk(string, type='*'):
    if string == '':
        return r'.*'
    else:
        return str(int(string))

def getPkExact(string, type='*'):
    if string == '':
        return ''
    else:
        return str(int(string))