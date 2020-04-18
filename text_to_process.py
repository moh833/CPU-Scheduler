
def proc_from_text(data):
    '''takes text and returns list of processes or number of the line that caused an error if happens'''
    data = data.strip().split('\n')
    n = len(data)
    proc = []
    for i in range(n):
        p = dict()
        try:
            p['id'] = i
            p['at'], p['bt'] = map(float, data[i].split())
            proc.append(p)
        except:
            print("try again, error in line", i+1)
            return i+1
    return proc


def proc_from_text_priority(data):
    '''takes text and returns list of processes or number of the line that caused an error if happens'''
    data = data.strip().split('\n')
    n = len(data)
    proc = []
    for i in range(n):
        p = dict()
        try:
            p['id'] = i
            p['at'], p['bt'], p['p'] = map(float, data[i].split())
            proc.append(p)
        except:
            print("try again, error in line", i+1)
            return i+1
    return proc