import copy

def priority_p(proc):
    n = len(proc)
    temp = copy.deepcopy(proc)
    temp.sort(key=lambda l: l['at'])
    hold = []
    chart = []
    i = 0
    cur_time = 0.0
    wasted = temp[0]['at'] - cur_time
    if wasted > 0.0:
        chart.append([-1, wasted])
    cur_time = temp[0]['at']
    hold.append(0)
    while(i<n):
        if not hold:
            wasted = temp[i+1]['at'] - cur_time
            if(wasted > 0.0):
                i += 1
                chart.append([-1, wasted])
                cur_time = temp[i]['at']
                hold.append(i)
        while(i+1 < n and cur_time == temp[i+1]['at']):
            hold.append(i+1)
            i += 1

        if(i == n-1):
            break

        cur_proc_ind, cur_proc = min([[i, temp[i]] for i in hold], key=lambda x:x[1]['p'])
        work_time = temp[i+1]['at'] - cur_time
        if(cur_proc['bt'] <= work_time):
            if(chart and chart[-1][0] == cur_proc['id']):
                chart[-1][1] += cur_proc['bt']
            else:
                chart.append([cur_proc['id'], cur_proc['bt']])
            proc[cur_proc['id']]['wt'] = cur_time - (proc[cur_proc['id']]['bt'] - cur_proc['bt']) - cur_proc['at']
            proc[cur_proc['id']]['tat'] = proc[cur_proc['id']]['wt'] + proc[cur_proc['id']]['bt']
            cur_time += cur_proc['bt']
            cur_proc['bt'] = 0
            hold.remove(cur_proc_ind)
        else:
            if(chart and chart[-1][0] == cur_proc['id']):
                chart[-1][1] += work_time
            else:
                chart.append([cur_proc['id'], work_time])
            cur_proc['bt'] -= work_time
            cur_time += work_time

        temp[cur_proc_ind] = cur_proc
    ####################
    while(hold):
        cur_proc_ind, cur_proc = min([[i, temp[i]] for i in hold], key=lambda x:x[1]['p'])
        if(chart and chart[-1][0] == cur_proc['id']):
            chart[-1][1] += cur_proc['bt']
        else:
            chart.append([cur_proc['id'], cur_proc['bt']])
        cur_time += cur_proc['bt']
        proc[cur_proc['id']]['wt'] = cur_time - cur_proc['at'] - proc[cur_proc['id']]['bt']
        proc[cur_proc['id']]['tat'] = proc[cur_proc['id']]['wt'] + proc[cur_proc['id']]['bt']
        cur_proc['bt'] = 0
        hold.remove(cur_proc_ind)
        temp[cur_proc_ind] = cur_proc
    return proc, chart