
import copy

def sjf_non(proc):
  n = len(proc)

  temp = copy.deepcopy(proc)
  temp.sort(key=lambda l: l['at'])
  chart = []


  cur_time = temp[0]['at']
  hold = [0]
  last_ind = 1

  while(last_ind < n):
    if(not hold):
      wasted = temp[last_ind]['at'] - cur_time
      if(wasted > 0):
        chart.append([-1, wasted])
        cur_time = temp[last_ind]['at']
    while(last_ind < n and temp[last_ind]['at'] <= cur_time):
      hold.append(last_ind)
      last_ind += 1

    cur_proc_ind, cur_proc = min([[i, temp[i]] for i in hold], key=lambda x:x[1]['bt'])

    proc[cur_proc['id']]['wt'] = cur_time - cur_proc['at']
    proc[cur_proc['id']]['tat'] = proc[cur_proc['id']]['wt'] + cur_proc['bt']

    chart.append([cur_proc['id'], cur_proc['bt']])
    cur_time += cur_proc['bt']
    hold.remove(cur_proc_ind)

  while(hold):
    cur_proc_ind, cur_proc = min([[i, temp[i]] for i in hold], key=lambda x:x[1]['bt'])

    proc[cur_proc['id']]['wt'] = cur_time - cur_proc['at']
    proc[cur_proc['id']]['tat'] = proc[cur_proc['id']]['wt'] + cur_proc['bt']

    chart.append([cur_proc['id'], cur_proc['bt']])
    cur_time += cur_proc['bt']
    hold.remove(cur_proc_ind)


  return proc, chart

