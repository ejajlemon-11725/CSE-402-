#include <bits/stdc++.h>
using namespace std;

struct Process {
    string pid;
    int arrival_time;
    int burst_time;
    int completion_time;
    int turnaround_time;
    int waiting_time;
    bool completed;
};

int main() {
    int num_processes;
    cout << "Enter the number of processes: ";
    cin >> num_processes;

    vector<Process> processes(num_processes);

    cout << "Enter PID, Arrival Time, Burst Time for each process:\n";
    for (int i = 0; i < num_processes; i++) {
        cin >> processes[i].pid >> processes[i].arrival_time >> processes[i].burst_time;
        processes[i].completed = false;
    }

    int current_time = 0;
    int completed_processes = 0;

    while (completed_processes < num_processes) {
        int shortest_job = -1;
        int min_burst_time = INT_MAX;

        for (int i = 0; i < num_processes; i++) {
            if (!processes[i].completed &&
                processes[i].arrival_time <= current_time &&
                processes[i].burst_time < min_burst_time) {
                min_burst_time = processes[i].burst_time;
                shortest_job = i;
            }
        }

        if (shortest_job == -1) {
            int next_arrival = INT_MAX;
            for (int i = 0; i < num_processes; i++) {
                if (!processes[i].completed && processes[i].arrival_time > current_time) {
                    next_arrival = min(next_arrival, processes[i].arrival_time);
                }
            }
            current_time = next_arrival;
        } else {
            current_time += processes[shortest_job].burst_time;
            processes[shortest_job].completion_time = current_time;
            processes[shortest_job].turnaround_time = processes[shortest_job].completion_time - processes[shortest_job].arrival_time;
            processes[shortest_job].waiting_time = processes[shortest_job].turnaround_time - processes[shortest_job].burst_time;
            processes[shortest_job].completed = true;
            completed_processes++;
        }
    }

    cout << "\nPID\tAT\tBT\tCT\tTAT\tWT\n";
    double total_waiting = 0, total_turnaround = 0;

    for (const auto &p : processes) {
        cout << p.pid << "\t" << p.arrival_time << "\t" << p.burst_time << "\t"
             << p.completion_time << "\t" << p.turnaround_time << "\t" << p.waiting_time << endl;
        total_waiting += p.waiting_time;
        total_turnaround += p.turnaround_time;
    }

    cout << fixed << setprecision(2);
    cout << "\nAverage Waiting Time: " << total_waiting / num_processes << endl;
    cout << "Average Turnaround Time: " << total_turnaround / num_processes << endl;

    return 0;
}
