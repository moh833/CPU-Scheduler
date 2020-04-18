import copy

def fcfs(proc):
    n = len(proc)

    temp = copy.deepcopy(proc)
    temp.sort(key=lambda l: l['at'])

    chart = []
    i = 0
    cur_time = temp[0]['at']

    for i in range(n):
        cur_proc = temp[i]
        if(cur_time < cur_proc['at']):
            wasted = cur_proc['at'] - cur_time
            chart.append([-1, wasted])
            cur_time += wasted
        
        chart.append([cur_proc['id'], cur_proc['bt']])

        proc[cur_proc['id']]['wt'] = cur_time - cur_proc['at']
        proc[cur_proc['id']]['tat'] = proc[cur_proc['id']]['wt'] + cur_proc['bt']
    
        cur_time += cur_proc['bt']

    return proc, chart