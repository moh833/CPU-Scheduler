import matplotlib.pyplot as plt 
import numpy as np

def draw_chart(chart, n, max_time, diff_colors: bool):

    fig, ax = plt.subplots()

    ax.set_xlim(0, max_time)
    ax.set_ylim(0, 2*n)

    ax.set_xlabel('Time')
    ax.set_ylabel('Process ID')

    ax.set_yticks(range(1, 2*n, 2))
    # ax.set_yticklabels(range(1, n+1))
    ax.set_yticklabels([f"P{i}" for i in range(1, n+1)])

    ax.grid(True)

    start = 0

    if diff_colors:
        colors = plt.cm.rainbow(np.linspace(0,1,n))

        for c in chart:
            if c[0] == -1:
                start += c[1]
                continue
            ax.broken_barh([(start, c[1])], (c[0]*2+0.25, 1.5), facecolors=colors[c[0]])
            start += c[1]
    else:
        for c in chart:
            if c[0] == -1:
                start += c[1]
                continue
            ax.broken_barh([(start, c[1])], (c[0]*2+0.25, 1.5), facecolors='blue')
            start += c[1]

    plt.savefig('graph.png', dpi=100, bbox_inches='tight')


def draw_pie(proc, n, str_time):

    fig, ax = plt.subplots()
    
    if(str_time=='wt'):
        title = 'Waiting Time'
    elif(str_time=='bt'):
        title = 'Burst Time'
    elif(str_time=='tat'):
        title = 'Turnaround Time'
    else:
        print('unsupported')
        exit(1)

    labels = []
    times = []
    for i in range(n):
        if(proc[i][str_time] > 0.0):
            labels.append(f"P{i+1}")
            times.append(proc[i][str_time])

    ax.pie(times, labels=labels, autopct='%1.1f%%')
    ax.set_title(title, pad=30)
    ax.axis('equal') 

    plt.savefig('graph.png', dpi=100, bbox_inches='tight')


def draw_bar(proc, n, str_time):
    
    fig, ax = plt.subplots()

    labels = [f"P{i}" for i in range(1, n+1)]
    times = [p[str_time] for p in proc]

    ax.bar(labels, times)
    plt.savefig('graph.png', dpi=100, bbox_inches='tight')


def draw_bars(proc, n):

    fig, ax = plt.subplots()

    centers = np.arange(1, 2*n, 2)
    width = 0.7


    labels = [f"P{i}" for i in range(1, n+1)]

    times_1 = [p['bt'] for p in proc]
    label_1 = "Burst Time"
    times_2 = [p['wt'] for p in proc]
    label_2 = "Waiting Time"
    title = 'Burst and Waiting Time'


    ax.set_xticks(centers)
    ax.set_xticklabels(labels)

    ax.set_ylabel('Time')
    ax.set_title(title)


    rects1 = ax.bar(centers - width/2, times_1, width, label=label_1)
    rects2 = ax.bar(centers + width/2, times_2, width, label=label_2)

    ax.legend()
    fig.tight_layout()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(rects1)
    autolabel(rects2)

    plt.savefig('graph.png', dpi=100, bbox_inches='tight')