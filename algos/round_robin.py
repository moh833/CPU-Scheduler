import copy

def round_robin(proc, unit_time):
  n = len(proc)

  temp = copy.deepcopy(proc)
  temp.sort(key=lambda l: l['at'])

  hold = []
  chart = []

  i = 0
  cur_time = 0.0
  done = False
  while(True):

    # if we took all the processes and there is no process on hold
    if(i==n and not hold):
      break

    if(not hold):
      wasted = temp[i]['at'] - cur_time
      if(wasted > 0):
        chart.append([-1, wasted])
        cur_time = temp[i]['at']
        hold.append(i)
        i += 1

    while(i < n and cur_time >= temp[i]['at']):
      if(hold and not done):
        hold.insert(-1, i)
      else:
        hold.append(i)
      i += 1


    cur_proc_ind = hold[0]
    cur_proc = temp[cur_proc_ind]

    # will finish
    if(cur_proc['bt'] <= unit_time):
      if(chart and chart[-1][0] == cur_proc['id']):
        chart[-1][1] += cur_proc['bt']
      else:
        chart.append([cur_proc['id'], cur_proc['bt']])
      
      cur_time += cur_proc['bt']

      proc[cur_proc['id']]['wt'] = cur_time - cur_proc['at'] - proc[cur_proc['id']]['bt']
      proc[cur_proc['id']]['tat'] = proc[cur_proc['id']]['wt'] + proc[cur_proc['id']]['bt']

      cur_proc['bt'] = 0

      del hold[0]
      done = True
    else:
      if(chart and chart[-1][0] == cur_proc['id']):
        chart[-1][1] += unit_time
      else:
        chart.append([cur_proc['id'], unit_time])
      
      cur_time += unit_time
      cur_proc['bt'] -= unit_time

      hold.append(hold.pop(0))
      done = False
    
    # general
    temp[cur_proc_ind] = cur_proc


  return proc, chart

