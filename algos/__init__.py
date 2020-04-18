from algos.FCFS import fcfs
from algos.SJF_p import sjf_p
from algos.SJF_non import sjf_non
from algos.priority_p import priority_p
from algos.priority_non import priority_non
from algos.round_robin import round_robin

def run_algo(proc, algo, unit_time=1.0):
    if(algo == 'FCFS'):
        return fcfs(proc)
    elif(algo == 'SJF_P'):
        return sjf_p(proc)
    elif(algo == 'SJF_N'):
        return sjf_non(proc)
    elif(algo == 'PR_P'):
        return priority_p(proc)
    elif(algo == 'PR_N'):
        return priority_non(proc)
    elif(algo == 'RR'):
        return round_robin(proc, unit_time)
    else:
        print("unsupported algorithm")
        exit(2)
