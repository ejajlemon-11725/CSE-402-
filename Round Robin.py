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
n = len(processes)
remaining = [p[2] for p in processes]
ct = [0] * n
queue = deque()
time = 0
completed = 0
visited = [False] * n
gnatt = []
while completed < n:
    for i in range(n):
        if processes[i][1] <= time and not visited[i]:
            queue.append(i)
            visited[i] = True
    if not queue:
        next_time = min(
            processes[i][1]
            for i in range(n)
            if not visited[i]
        )
        time = next_time
        continue
    i = queue.popleft()
    start_time = time
    execution_time = min(time_quantum, remaining[i])
    time += execution_time
    remaining[i] -= execution_time
    gnatt.append((processes[i][0], start_time, time))
    for j in range(n):
        if processes[j][1] <= time and not visited[j]:
            queue.append(j)
            visited[j] = True
    if remaining[i] > 0:
        queue.append(i)
    else:
        ct[i] = time
        completed += 1
tat = [0] * n
wt = [0] * n

for i in range(n):
    tat[i] = ct[i] - processes[i][1]
    wt[i] = tat[i] - processes[i][2]
print("\nProcess\tAT\tBT\tCT\tTAT\tWT")
for i in range(n):
    print(
        f"{processes[i][0]}\t"
        f"{processes[i][1]}\t"
        f"{processes[i][2]}\t"
        f"{ct[i]}\t"
        f"{tat[i]}\t"
        f"{wt[i]}"
    )
avg_tat = sum(tat) / n
avg_wt = sum(wt) / n
print("\nAverage Turnaround Time:", avg_tat)
print("Average Waiting Time:", avg_wt)
print("\nGnatt Chart:")
for process, start, end in gnatt:
    print(f"| {process} ", end="")
print("|")
for process, start, end in gnatt:
    print(f"{start:<4}", end="")
print(time)