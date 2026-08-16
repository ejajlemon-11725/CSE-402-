from collections import deque
processes = [
    ["P1", 0, 7],
    ["P2", 1, 4],
    ["P3", 2, 15],
    ["P4", 3, 11],
    ["P5", 4, 20],
    ["P6", 4, 9]
]
time_quantum = 5
def fcfs(processes):
    time = 0
    result = []
    for pid, at, bt in processes:
        if time < at:
            time = at
        ct = time + bt
        tat = ct - at
        wt = tat - bt
        result.append([pid, at, bt, ct, tat, wt])
        time = ct
    return result
    
def sjf(processes):
    remaining = processes.copy()
    result = []
    time = 0
    while remaining:
        available = [
            p for p in remaining
            if p[1] <= time
        ]
        if not available:
            time = min(p[1] for p in remaining)
            continue
        process = min(
            available,
            key=lambda p: (p[2], p[1])
        )
        pid, at, bt = process
        ct = time + bt
        tat = ct - at
        wt = tat - bt
        result.append([pid, at, bt, ct, tat, wt])
        time = ct
        remaining.remove(process)
    return result

def round_robin(processes, quantum):

    n = len(processes)

    remaining = [p[2] for p in processes]
    ct = [0] * n

    queue = deque()

    visited = [False] * n

    time = 0
    completed = 0

    while completed < n:
        for i in range(n):
            if processes[i][1] <= time and not visited[i]:
                queue.append(i)
                visited[i] = True

        if not queue:
            time = min(
                processes[i][1]
                for i in range(n)
                if not visited[i]
            )
            continue

        i = queue.popleft()

        execution_time = min(
            quantum,
            remaining[i]
        )

        time += execution_time
        remaining[i] -= execution_time

        for j in range(n):
            if processes[j][1] <= time and not visited[j]:
                queue.append(j)
                visited[j] = True

        if remaining[i] > 0:
            queue.append(i)

        else:
            ct[i] = time
            completed += 1

    result = []

    for i in range(n):

        pid = processes[i][0]
        at = processes[i][1]
        bt = processes[i][2]

        tat = ct[i] - at
        wt = tat - bt

        result.append([
            pid, at, bt, ct[i], tat, wt
        ])

    return result


def print_result(name, result):

    print("\n" + "=" * 55)
    print(name)
    print("=" * 55)

    print("Process\tAT\tBT\tCT\tTAT\tWT")

    for r in result:
        print(
            f"{r[0]}\t"
            f"{r[1]}\t"
            f"{r[2]}\t"
            f"{r[3]}\t"
            f"{r[4]}\t"
            f"{r[5]}"
        )

    avg_tat = sum(r[4] for r in result) / len(result)
    avg_wt = sum(r[5] for r in result) / len(result)

    print("\nAverage Turnaround Time =", round(avg_tat, 2))
    print("Average Waiting Time    =", round(avg_wt, 2))

    return avg_tat, avg_wt
  

fcfs_result = fcfs(processes)

sjf_result = sjf(processes)

rr_result = round_robin(
    processes,
    time_quantum
)


fcfs_tat, fcfs_wt = print_result(
    "FCFS",
    fcfs_result
)

sjf_tat, sjf_wt = print_result(
    "SJF",
    sjf_result
)

rr_tat, rr_wt = print_result(
    "ROUND ROBIN (Time Quantum = 5)",
    rr_result
)



print("\n" + "=" * 65)
print("PERFORMANCE COMPARISON")
print("=" * 65)

print("\nAlgorithm\tAverage WT\tAverage TAT")

print(
    f"FCFS\t\t{fcfs_wt:.2f}\t\t{fcfs_tat:.2f}"
)

print(
    f"SJF\t\t{sjf_wt:.2f}\t\t{sjf_tat:.2f}"
)

print(
    f"Round Robin\t{rr_wt:.2f}\t\t{rr_tat:.2f}"
)



algorithms = {
    "FCFS": fcfs_wt,
    "SJF": sjf_wt,
    "Round Robin": rr_wt
}

best = min(algorithms, key=algorithms.get)

print("\n" + "=" * 65)
print("BEST PERFORMANCE")
print("=" * 65)

print(
    f"Best Algorithm = {best}"
)

print(
    f"Lowest Average Waiting Time = "
    f"{algorithms[best]:.2f}"
)