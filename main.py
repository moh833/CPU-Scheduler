from PyQt5 import QtCore, QtGui, QtWidgets
from design import Ui_MainWindow

from text_to_process import proc_from_text, proc_from_text_priority
from draw import draw_chart, draw_pie, draw_bar, draw_bars
from algos import run_algo

encoding = {0: 'FCFS',
            1: 'SJF_P',
            2: 'SJF_N',
            3: 'PR_P',
            4: 'PR_N',
            5: 'RR'}

infos = {'FCFS': 'First Come, First Served (FCFS)\n\nAutomatically executes queued requests and processes by the order of their arrival.\n\n\n\nPlease Enter the arrival time then burst time seperated by space for each process in a seperate lines.',
         'SJF_P': 'Shortest Job First (SJF): Preemptive\n\nThe process having the smallest execution time is chosen for the next execution.\nJobs are put into the ready queue as they come. A process with shortest burst time begins execution. If a process with even a shorter burst time arrives, the current process is removed or preempted from execution, and the shorter job is allocated CPU cycle.\n\n\n\nPlease Enter the arrival time then burst time seperated by space for each process in a seperate lines.',
         'SJF_N': 'Shortest Job First (SJF): Non-Preemptive\n\nThe process having the smallest execution time is chosen for the next execution.\nOnce the CPU cycle is allocated to process, the process holds it till it reaches a waiting state or terminated.\n\n\n\nPlease Enter the arrival time then burst time seperated by space for each process in a seperate lines.',
         'PR_P': 'Priority: Preemptive\n\nEach process is assigned a priority. Process with highest priority is to be executed first and so on.\nProcesses with same priority are executed on first come first served basis.\nThe task with a higher priority runs before another lower priority task, even if the lower priority task is still running.\n\n\n\nPlease Enter the arrival time, burst time then priority seperated by space for each process in a seperate lines.',
         'PR_N': 'Priority: Non-Preemptive\n\nEach process is assigned a priority. Process with highest priority is to be executed first and so on.\nProcesses with same priority are executed on first come first served basis.\nThe process that keeps the CPU busy, will release the CPU either by switching context or terminating.\n\n\n\nPlease Enter the arrival time, burst time then priority seperated by space for each process in a seperate lines.',
         'RR': 'Round-Robin\n\nEach ready task runs turn by turn only in a cyclic queue for a limited time slice. This algorithm also offers starvation free execution of processes.\n\n\n\nPlease Enter the arrival time then burst time seperated by space for each process in a seperate lines and specify the time slice in the box below.'}

gragh_encoding = {0: 'gantt',
                  1: 'pie',
                  2: 'bar'}

graph_choices = {'gantt':['Different Colors', 'One Color'],
                 'pie': ['Wating Time', 'Turnaround Time', 'Burst Time'],
                 'bar': ['Wating Time', 'Turnaround Time', 'Burst Time', 'Burst and Waiting Time']}


class MainClass(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow); 
        self.load_btn.clicked.connect(self.load_file)
        self.clear_btn.clicked.connect(self.clear_code)
        self.run_btn.clicked.connect(self.run_code)
        self.draw_btn.clicked.connect(self.draw_code)

        self.info_text.setText(infos[encoding[0]])

        self.proc_combo.currentIndexChanged.connect(self.on_proc_changed)
        self.graphs_combo.currentIndexChanged.connect(self.on_graph_changed)

        self.unit_time_line.hide()
        self.unit_time_lbl.hide()

        MainWindow.setWindowIcon(QtGui.QIcon('cpu.ico'))


    
    def load_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget)
        if filename[0]:
            with open(filename[0], 'r') as file:
                data = file.read()
                self.input_text.setPlainText(data)
    
    def clear_code(self):
        self.input_text.setPlainText('')

    def run_code(self):
        global proc, chart
        index = self.proc_combo.currentIndex()
        data = self.input_text.toPlainText()
        unit_time = 1
        self.warning_text.setText('')

        if(encoding[index] in ['PR_P', 'PR_N']):
            proc = proc_from_text_priority(data)
        else:
            proc = proc_from_text(data)
        # if the type is int then it's the line number that caused an error
        if type(proc) is int:
            self.warning_text.setText(f"There is an error in line {proc}, Please make sure the input as specified and try again!")
            data = data.strip().split('\n')
            self.input_text.setPlainText('\n'.join(data[:proc-1]))
            # self.input_text.appendHtml(f'<font color="red">{data[proc-1]}</font>')
            self.input_text.appendHtml(f'<span style="color:#ff002b";>{data[proc-1]}</span>')
            # self.input_text.appendHtml(f'<span style="background-color:#ff4d4d";>{data[proc-1]}</span>')
            self.input_text.appendPlainText ('\n'.join(data[proc:]))

            return
        # handle time_unit in round robin
        if(encoding[index] == 'RR'):
            try:
                unit_time = float(self.unit_time_line.text())
            except:
                self.warning_text.setText("Please enter unit time as a number and try again!")
                return
        proc, chart = run_algo(proc, encoding[index], unit_time)
        self.warning_text.setText("Success! Go to Graphs for more!")

        n = len(proc)
        avg_waiting = sum([p['wt'] for p in proc]) / n
        avg_turnaround = sum([p['tat'] for p in proc]) / n

        wasted_time = 0
        for c in chart:
            if c[0] == -1:
                wasted_time += c[1]
        
        self.graph_text.setText(f'Number of Processes: {n}\n')
        self.graph_text.append(f'Average Waiting Time: {avg_waiting:.2f}\n')
        self.graph_text.append(f'Avergae Turnaround Time: {avg_turnaround:.2f}\n')
        self.graph_text.append(f'Wasted Processing Time: {wasted_time:.2f}')

        self.graph_area.setPixmap(QtGui.QPixmap(""))


    def on_proc_changed(self, index):
        self.info_text.setText(infos[encoding[index]])
        if(encoding[index] == 'RR'):
            self.unit_time_line.show()
            self.unit_time_lbl.show()
        else:
            self.unit_time_line.hide()
            self.unit_time_lbl.hide()


    def on_graph_changed(self, index):
        self.options_combo.clear()       # delete all items from comboBox
        self.options_combo.addItems(graph_choices[gragh_encoding[index]])

    
    def draw_code(self):
        if 'chart' not in globals() or 'proc' not in globals():
            self.graph_text.setText("Please run a process before graphing!")
            return
        else:
            n = len(proc)

            graph_id = self.graphs_combo.currentIndex()
            option_id =self.options_combo.currentIndex()

            if gragh_encoding[graph_id] == 'gantt':
                max_time = proc[chart[-1][0]]['tat'] + proc[chart[-1][0]]['at']
                if option_id == 0:
                    draw_chart(chart, n, max_time, True)
                else:
                    draw_chart(chart, n, max_time, False)
                self.graph_area.setPixmap(QtGui.QPixmap("graph.png"))
            elif gragh_encoding[graph_id] == 'pie':
                if option_id == 0:
                    draw_pie(proc, n, 'wt')
                elif option_id == 1:
                    draw_pie(proc, n, 'tat')
                else:
                    draw_pie(proc, n, 'bt')
                self.graph_area.setPixmap(QtGui.QPixmap("graph.png"))
            elif gragh_encoding[graph_id] == 'bar':
                if option_id == 0:
                    draw_bar(proc, n, 'wt')
                elif option_id == 1:
                    draw_bar(proc, n, 'tat')
                elif option_id == 2:
                    draw_bar(proc, n, 'bt')
                else:
                    draw_bars(proc, n)
                self.graph_area.setPixmap(QtGui.QPixmap("graph.png"))
            else:
                print('unsupported operation')
            


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainClass()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())