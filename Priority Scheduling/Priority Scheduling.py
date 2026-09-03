processes = [
    {"pid": "P1", "at": 0, "priority": 3, "bt": 3},
    {"pid": "P2", "at": 1, "priority": 2, "bt": 4},
    {"pid": "P3", "at": 2, "priority": 4, "bt": 6},
    {"pid": "P4", "at": 3, "priority": 6, "bt": 4},
    {"pid": "P5", "at": 5, "priority": 10, "bt": 2}
]

def non_preemptive(processes):
    p = [x.copy() for x in processes]
    time = 0
    completed = 0
    n = len(p)
    result = []
    gantt = []
    for x in p:
        x["completed"] = False

    while completed < n:
        available = []
        for x in p:
            if x["at"] <= time and x["completed"] == False:
                available.append(x)
        if not available:
            time += 1
            continue
        available.sort(key=lambda x: (x["priority"], x["at"]))
        current = available[0]
        pid = current["pid"]
        at = current["at"]
        priority = current["priority"]
        bt = current["bt"]
        start = time
        time += bt
        ct = time
        tat = ct - at
        wt = tat - bt
        current["completed"] = True
        result.append([
            pid, at, bt, priority, ct, tat, wt
        ])
        gantt.append([pid, start, ct])
        completed += 1
    return result, gantt

def preemptive(processes):
    p = [x.copy() for x in processes]
    n = len(p)
    time = 0
    completed = 0
    for x in p:
        x["rt"] = x["bt"]
        x["ct"] = 0
    gantt = []
    
    while completed < n:
        available = []
        for x in p:
            if x["at"] <= time and x["rt"] > 0:
                available.append(x)
        if not available:
            time += 1
            continue
        available.sort(key=lambda x: (x["priority"], x["at"]))
        current = available[0]
        pid = current["pid"]
        if len(gantt) == 0 or gantt[-1][0] != pid:
            gantt.append([pid, time, time + 1])
        else:
            gantt[-1][2] = time + 1
        current["rt"] -= 1
        time += 1

        if current["rt"] == 0:
            current["ct"] = time
            completed += 1
    result = []
    for x in p:
        pid = x["pid"]
        at = x["at"]
        bt = x["bt"]
        priority = x["priority"]
        ct = x["ct"]
        tat = ct - at
        wt = tat - bt
        result.append([
            pid, at, bt, priority, ct, tat, wt
        ])
    return result, gantt


def display(title, result, gantt):
    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)
    print("\nGantt Chart:")
    for g in gantt:
        print(f"| {g[0]} ", end="")
    print("|")
    print(gantt[0][1], end="")
    for g in gantt:
        print(f"    {g[2]}", end="")
    print()
    print("\nPID\tAT\tBT\tPriority\tCT\tTAT\tWT")
    total_tat = 0
    total_wt = 0
    for r in result:
        print(
            f"{r[0]}\t{r[1]}\t{r[2]}\t"
            f"{r[3]}\t\t{r[4]}\t{r[5]}\t{r[6]}"
        )
        total_tat += r[5]
        total_wt += r[6]
    n = len(result)
    avg_tat = total_tat / n
    avg_wt = total_wt / n
    print("\nAverage TAT =", round(avg_tat, 2))
    print("Average WT  =", round(avg_wt, 2))
    return avg_tat, avg_wt
non_result, non_gantt = non_preemptive(processes)
pre_result, pre_gantt = preemptive(processes)
non_tat, non_wt = display(
    "PRIORITY SCHEDULING - NON-PREEMPTIVE",
    non_result,
    non_gantt
)

pre_tat, pre_wt = display(
    "PRIORITY SCHEDULING - PREEMPTIVE",
    pre_result,
    pre_gantt
)

print("\n" + "=" * 65)
print("PERFORMANCE COMPARISON")
print("=" * 65)

print("Non-Preemptive Average WT :", round(non_wt, 2))
print("Preemptive Average WT     :", round(pre_wt, 2))

print("Non-Preemptive Average TAT:", round(non_tat, 2))
print("Preemptive Average TAT    :", round(pre_tat, 2))

if pre_wt < non_wt:
    print("\nPreemptive has better performance than Non-Preemptive")
elif non_wt < pre_wt:
    print("\nNon-Preemptive has better performance than Preemptive")
else:
    print("\nBoth have the same performance")