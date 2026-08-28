TQ = 2
processes = [
    {"pid": "P1", "at": 4, "bt": 2},
    {"pid": "P2", "at": 2, "bt": 2},
    {"pid": "P3", "at": 1, "bt": 3},
    {"pid": "P4", "at": 0, "bt": 6},
    {"pid": "P5", "at": 3, "bt": 1}
]

for p in processes:
    p["rem"] = p["bt"]
    p["ct"] = 0
    p["tat"] = 0
    p["wt"] = 0
time = 0
completed = 0
n = len(processes)
gantt = []

while completed < n:
    available = [
        p for p in processes
        if p["at"] <= time and p["rem"] > 0
    ]
    if not available:
        time += 1
        continue
    current = min(
        available,
        key=lambda p: (p["rem"], p["at"], p["pid"])
    )
    run_time = min(TQ, current["rem"])

    start = time

    current["rem"] -= run_time
    time += run_time
    gantt.append((start, time, current["pid"]))

    if current["rem"] == 0:
        current["ct"] = time
        current["tat"] = current["ct"] - current["at"]
        current["wt"] = current["tat"] - current["bt"]
        completed += 1

print("\nSJF Preemptive")
print("Time Quantum =", TQ)
print("\nPID\tAT\tBT\tCT\tTAT\tWT")
print("-" * 50)
total_tat = 0
total_wt = 0

for p in sorted(processes, key=lambda x: x["pid"]):
    print(
        f'{p["pid"]}\t'
        f'{p["at"]}\t'
        f'{p["bt"]}\t'
        f'{p["ct"]}\t'
        f'{p["tat"]}\t'
        f'{p["wt"]}'
    )
    total_tat += p["tat"]
    total_wt += p["wt"]
print("-" * 50)
print(f"Average TAT = {total_tat / n:.2f}")
print(f"Average WT  = {total_wt / n:.2f}")
print("\nGantt Chart:")
for start, end, pid in gantt:
    print(f"{start} -> {end}: {pid}")