from prettytable import PrettyTable

table = PrettyTable()


table = PrettyTable()

table.field_names = ["Scheduling Algorithm"]

table.add_row(["1. Banker's Algorithm"])
table.add_row(["2. First Come First Serve (FCFS)"])
table.add_row(["3. Priority (Non-Preemptive)"])
table.add_row(["4. Priority (Preemptive)"])
table.add_row(["5. Round Robin"])
table.add_row(["6. Shortest Job First (SJF - Non-Preemptive)"])
table.add_row(["7. Shortest Job First (SJF - Preemptive)"])

table.align["Scheduling Algorithm"] = "c"

print(table)

choice = int(input("Your choice: "))

if choice == 1:
    from prettytable import PrettyTable

    class Process:
        def __init__(self):
            self.all = [0] * r
            self.max = [0] * r
            self.need = [0] * r
            self.flag = 0

    n = int(input("Enter the number of processes: "))
    r = int(input("Enter the number of resources: "))

    f = [Process() for _ in range(n)]
    avail = [0] * r

    for i in range(n):
        print("Enter details for P{}".format(i))
        print("Enter allocation: ", end="")
        f[i].all = list(map(int, input().split()))
        print("Enter Max: ", end="")
        f[i].max = list(map(int, input().split()))
        f[i].flag = 0

    print("Enter Available Resources: ", end="")
    avail = list(map(int, input().split()))

    for i in range(n):
        for j in range(r):
            f[i].need[j] = f[i].max[j] - f[i].all[j]
            if f[i].need[j] < 0:
                f[i].need[j] = 0

    cnt = 0
    fl = 0
    seq = []

    while cnt != n:
        g = 0
        for j in range(n):
            if f[j].flag == 0:
                b = 0
                for p in range(r):
                    if avail[p] >= f[j].need[p]:
                        b += 1
                if b == r:
                    seq.append(j)
                    f[j].flag = 1
                    for k in range(r):
                        avail[k] += f[j].all[k]
                    cnt += 1
                    print("P{} is visited".format(j))
                    print("(", end="")
                    for k in range(r):
                        print("{:3d}".format(avail[k]), end="")
                    print(")")
                    g = 1
        if g == 0:
            print("\nREQUEST NOT GRANTED -- DEADLOCK OCCURRED")
            print("SYSTEM IS IN UNSAFE STATE")
            break

    if cnt == n:
        print("\nSYSTEM IS IN SAFE STATE")
        print("The Safe Sequence is: (", end="")
        for i in seq:
            print("P{} ".format(i), end="")
        print(")")

    table = PrettyTable()
    table.field_names = ["Process", "Allocation", "Max", "Need"]
    for i in range(n):
        allocation = " ".join(str(x) for x in f[i].all)
        max_resources = " ".join(str(x) for x in f[i].max)
        need = " ".join(str(x) for x in f[i].need)
        table.add_row(["P{}".format(i), allocation, max_resources, need])

    print(table)


elif choice == 2:
    from prettytable import PrettyTable
    import matplotlib.pyplot as plt

    num = int(input("Please Enter Number of Processes: "))
    process_lst = []
    process_names = []
    average_WT = 0
    average_TAT = 0

    for i in range(num):
        arrival_time = int(input(f"Please Input Arrival time for P{i+1}: "))
        burst_time = int(input(f"Please Input Burst Time for P{i+1}: "))
        process_lst.append([arrival_time, burst_time])
        process_names.append(f"P{i+1}")

    sorted_lst = sorted(process_lst, key=lambda x: x[0])
    for val in sorted_lst:
        idx = process_lst.index(val)
        val.insert(0, process_names[idx])

    process_lst = []
    gantt_chart = []
    current_time = 0

    for i, val in enumerate(sorted_lst):
        pname, arrival_time, burst_time = val
        if current_time < arrival_time:
            current_time = arrival_time
        start_time = current_time
        completion_time = current_time + burst_time
        TAT = completion_time - arrival_time
        WT = TAT - burst_time
        average_WT += WT
        average_TAT += TAT
        process_lst.append([pname, arrival_time, burst_time, completion_time, TAT, WT])
        gantt_chart.append([pname, start_time, completion_time])
        current_time = completion_time

    pt = PrettyTable()
    pt.field_names = ["Process", "Arrival Time", "Burst Time", "Completion Time", "TAT", "WT"]
    pt.add_rows(process_lst)
    print(pt)
    print(f"Average Waiting Time: {average_WT / num}")
    print(f"Average Turn Around Time: {average_TAT / num}")

# Generate Gantt chart
    fig, ax = plt.subplots(figsize=(8, 3))
    for i, val in enumerate(gantt_chart):
        pno, start_time, end_time = val
        duration = end_time - start_time
        ax.broken_barh([(start_time, duration)], (10 * i, 9), facecolors="tab:blue", edgecolor='black')
        ax.text(start_time + duration / 2, 10 * i + 4.5, pno, ha="center", va="center")
    ax.set_xlim(0, gantt_chart[-1][2] + 2)
    ax.set_ylim(0, 10 * len(gantt_chart))
    ax.set_xlabel("Time")
    ax.set_yticks([])
    ax.set_title("Gantt Chart")
    plt.show()

    
elif choice == 3:
    from prettytable import PrettyTable
    import matplotlib.pyplot as plt

    def sortFunc(lst_process, lst_names):
        copy_names = lst_names[:]
        copy_lst = lst_process[:]
        new_lst = [[0, 0, 0]]   #Initializing CPU
        minVal = min(copy_lst, key = lambda x : x[0])   # To Find Out if the Processes Arrive at 0 or.
        remVal = minVal[0]

        tempFunc = lambda x : x[1]

        while copy_lst:
            temp = []
            currentTime = sum(map(tempFunc, new_lst)) + remVal

            for index, val in enumerate(copy_lst):
                at, bt, pt = val
                if at <= currentTime:
                    temp.append([at, bt, pt])

            minVal = min(temp, key = lambda x : x[2])  # Modified comparison for priority
            new_lst += [minVal]
            copy_lst.pop(copy_lst.index(minVal))

        new_lst.pop(0)
        return new_lst

    num = int(input("Please enter the number of processes: "))
    process_lst = []  # [[2, 6], [5, 2], [1, 8], [0, 3], [4, 4]]
    process_names = []  # ["P1", "P2", "P3", "P4", "P5"]

    for i in range(num):
        arrival_time = int(input(f"Please input the arrival time for P{i+1}: "))
        burst_time = int(input(f"Please input the burst time for P{i+1}: "))
        priority = int(input(f"Please input the priority of P{i+1}: "))
        process_names.append(f"P{i+1}")
        process_lst.append([arrival_time, burst_time, priority])

    sorted_process_lst = sortFunc(process_lst, process_names)
    for i, val in enumerate(sorted_process_lst):
        idx = process_lst.index(val)
        sorted_process_lst[i].insert(0, process_names[idx])

    new_process_lst = []
    average_WT = 0
    average_TAT = 0

    for i, val in enumerate(sorted_process_lst):
        pno, arrival, burst, priority = val
        completion_time = burst + arrival if len(new_process_lst) == 0 else burst + new_process_lst[i-1][4] if arrival < new_process_lst[i-1][4] else burst + new_process_lst[i-1][4] + (arrival - new_process_lst[i-1][4])
        TAT = completion_time - arrival
        WT = TAT - burst
        average_WT += WT
        average_TAT += TAT
        new_process_lst.append([pno, arrival, priority, burst, completion_time, TAT, WT])

    pt = PrettyTable()
    pt.field_names = ["Process", "Arrival Time", "Priority", "Burst Time", "Completion Time", "TAT", "WT"]
    pt.add_rows(new_process_lst)
    print(pt)
    print(f"Average Waiting Time: {average_WT / num}")
    print(f"Average Turnaround Time: {average_TAT / num}")
    
    # Generate Gantt chart
    fig, ax = plt.subplots(figsize=(8, 3))
    for i, val in enumerate(sorted_process_lst):
        pno, arrival, priority, burst, completion, tat, wt = val
        start_time = arrival if i == 0 else max(arrival, sorted_process_lst[i-1][4])
        end_time = completion
        duration = end_time - start_time
        ax.broken_barh([(start_time, duration)], (10 * i, 9), facecolors="tab:blue", edgecolor='black')
        ax.text(start_time + duration / 2, 10 * i + 4.5, pno, ha="center", va="center")
    ax.set_xlim(0, sorted_process_lst[-1][4] + 2)
    ax.set_ylim(0, 10 * len(sorted_process_lst))
    ax.set_xlabel("Time")
    ax.set_yticks([])
    ax.set_title("Gantt Chart")
    plt.show()

elif choice == 5:       
    from re import S
    from prettytable import PrettyTable  # For printing the result in a Tabular Format
    import matplotlib.pyplot as plt

    def sorting_burst(l):
        return l[2]  # Returns the Third element of the list which is Burst Time

    def sorting_arrival(l):
        return l[1]  # Returns the Second element of the list which is Arrival Time


    def Turn_Around_Time(P, limit):
        # Declaring Variables for Calculating Total Turn Around Time
        total_tat = 0
        for i in range(limit):
            tat = P[i][5] - P[i][1]
            total_tat += tat  # Formula For Turn Around Time -> Completion Time - Arrival Time
            P[i].append(tat)  # Appending the Turn Around Time to the List

        avg_tat = total_tat / limit
        return avg_tat


    def Waiting_Time(P, limit):
        # Declaring Variables for Calculating Total Waiting Time
        total_wt = 0

        for i in range(limit):
            wt = P[i][6] - P[i][4]
            total_wt += wt  # Formula For Waiting Time -> Turn Around Time - Burst Time
            P[i].append(wt)  # Appending the Waiting Time to the List

        avg_wt = total_wt / limit
        return avg_wt


    def Logic(P, limit, tq):
        completed_processes = []
        arrived = []  # Contains Processes which have completed their respective execution
        exit_time = []  # To note the completion time of a process -> the end time of the previous process + burst time of the  current process
        completion_time = 0  # Execution Time for a process

        # Sorting Processes by Arrival Time
        P.sort(key=sorting_arrival)

        while True:  # The loop runs until all the processes have been executed successfully
            not_arrived = []  # Contains Processes which have not completed their respective execution
            buffer = []

            for i in range(limit):
                if (P[i][1] <= completion_time and P[i][3] == 0):  # Checking whether the arrival time of the process is less
                    # than the Completion time or not and if the process has not been executed
                    a = 0
                    if (len(arrived) != 0):
                        for j in range(len(arrived)):
                            if (P[i][0] == arrived[j][0]):
                                a = 1

                    if a == 0:  # Adding a process once it's completed, to the Arrived list
                        buffer.extend([P[i][0], P[i][1], P[i][2], P[i][4]])  # Appending Process ID, AT, BT, and Burst Time, which
                        # will be used as Remaining Time - Time Quantum - Burst Time
                        arrived.append(buffer)
                        buffer = []

                    if (len(arrived) != 0 and len(completed_processes) != 0):  # Inserting a recently executed process at the
                        # end of the arrived list
                        for j in range(len(arrived)):
                            if (arrived[j][0] == completed_processes[len(completed_processes) - 1]):
                                arrived.insert((len(arrived) - 1), arrived.pop(j))

                elif P[i][3] == 0:
                    buffer.extend([P[i][0], P[i][1], P[i][2], P[i][4]])  # Appending Process ID, AT, BT, and Burst Time, which
                    # will be used as Remaining Time - Time Quantum - Burst Time
                    not_arrived.append(buffer)
                    buffer = []

            if len(arrived) == 0 and len(not_arrived) == 0:
                break

            if (len(arrived) != 0):
                if arrived[0][2] > tq:  # Process has Greater Burst Time than Time Quantum
                    completion_time += tq
                    exit_time.append(completion_time)
                    completed_processes.append(arrived[0][0])
                    for j in range(limit):
                        if (P[j][0] == arrived[0][0]):
                            break
                    P[j][2] -= tq  # Reducing Time Quantum from Burst time
                    arrived.pop(0)  # Popping the completed process

                elif (arrived[0][2] <= tq):  # If the Burst Time is Less than or Equal to Time Quantum
                    completion_time += arrived[0][2]
                    exit_time.append(completion_time)
                    completed_processes.append(arrived[0][0])
                    for j in range(limit):
                        if (P[j][0] == arrived[0][0]):
                            break

                    P[j][2] = 0  # Setting the Burst Time as 0 since the Process gets executed completely
                    P[j][3] = 1  # Setting Completion status as 1 -> implies the process has been executed successfully.
                    P[j].append(completion_time)
                    arrived.pop(0)  # Popping the completed process

            elif (len(arrived) == 0):
                if completion_time < not_arrived[0][1]:  # Checking the completion time with the arrival time of the process
                    # which hasn't been executed
                    completion_time = not_arrived[0][1]

                if not_arrived[0][2] > tq:  # Process has Greater Burst Time than Time Quantum
                    completion_time += tq
                    exit_time.append(completion_time)
                    completed_processes.append(not_arrived[0][0])
                    for j in range(limit):
                        if (P[j][0] == not_arrived[0][0]):
                            break
                    P[j][2] -= tq  # Reducing Time Quantum from Burst time

                elif (not_arrived[0][2] <= tq):  # If the Burst Time is Less than or Equal to Time Quantum
                    completion_time += not_arrived[0][2]
                    exit_time.append(completion_time)
                    completed_processes.append(not_arrived[0][0])
                    for j in range(limit):
                        if (P[j][0] == not_arrived[0][0]):
                            break

                    P[j][2] = 0  # Setting the Burst Time as 0 since the Process gets executed completely
                    P[j][3] = 1  # Setting Completion status as 1 -> implies the process has been executed successfully.
                    P[j].append(completion_time)

        tat = Turn_Around_Time(P, limit)
        wt = Waiting_Time(P, limit)

        P.sort(key=sorting_burst)  # Sorting the List by Burst Time (Order in which processes are executed)
        headers = ["Process Number", "Arrival Time", "Completion Time", "Turn Around Time", "Waiting Time"]
        table = [[p[0], p[1], p[5], p[6], p[7]] for p in P]
        pt = PrettyTable()
        pt.field_names = headers
        pt.add_rows(table)
        print(pt)
        gantt_chart = []
        process_index = {}
        for i, p in enumerate(P):
            process_index[p[0]] = i

        for i, p in enumerate(completed_processes):
            process_index_val = process_index[p]
            start_time = exit_time[completed_processes.index(p)]
            end_time = exit_time[i] if i < len(exit_time) else exit_time[i - 1] + P[process_index_val][6]
            gantt_chart.append((p, start_time, end_time))

        for i, p in enumerate(not_arrived):
            process_index_val = process_index[p[0]]
            start_time = p[1]
            end_time = completion_time
            gantt_chart.append((p[0], start_time, end_time))


        fig, ax = plt.subplots(figsize=(8, 3))
        for i, val in enumerate(gantt_chart, start=0):
            pno, start_time, end_time = val
            duration = end_time - start_time
            ax.broken_barh([(start_time, duration)], (10 * i, 9), facecolors="tab:blue", edgecolor='black')
            ax.text(start_time + duration / 2, 10 * i + 4.5, pno, ha="center", va="center")
        ax.set_xlim(0, gantt_chart[-1][2] + 2)
        ax.set_ylim(0, 10 * len(gantt_chart))
        ax.set_xlabel("Time")
        ax.set_yticks([])
        ax.set_title("Gantt Chart")
        plt.show()

        # Printing the Average Waiting and Turn Around Time
        print("\nAverage Waiting Time is = ", round(wt, 2))  # Rounding off Average Waiting Time to 2 Decimal places
        print("Average Turn Around Time is = ", round(tat, 2))  # Rounding off Average Turn Around Time to 2 Decimal places


    def main():
        run = True
        while (run):

            # Declaring arrays
            processes = []

            print("\nMenu\nDo you want to assume : \n1. Arrival Time as 0\n2. Input Arrival Time\n3. Exit\n")
            ch = int(input("Enter Your Choice : "))

            if ch == 1:
                limit_process = int(input("Enter the Number of Processes : "))
                for i in range(limit_process):
                    p = []
                    arrival = 0
                    burst = int(input("Enter the Burst Time for process {} : ".format(i)))
                    process_id = "P" + str(i + 1)

                    p.extend([process_id, arrival, burst, 0, burst])  # Forming a list of info entered by the user, 0 is for    completion status
                    processes.append(p)

                time_quantum = int(input("Enter the Time Quantum : "))  # Inputting Time Quantum from user

                Logic(processes, limit_process, time_quantum)
                run = int(input("\nWant to continue? (Yes = Input 1/false = Input 0) : "))

            elif ch == 2:
                limit_process = int(input("Enter the Number of Processes : "))
                for i in range(limit_process):
                    p = []
                    arrival = int(input("Enter the Arrival Time for process {} : ".format(i)))
                    burst = int(input("Enter the Burst Time for process {} : ".format(i)))
                    process_id = "P" + str(i + 1)

                    p.extend([process_id, arrival, burst, 0, burst])
                    processes.append(p)

                time_quantum = int(input("Enter the Time Quantum : "))  # Inputting Time Quantum from user

                Logic(processes, limit_process, time_quantum)
                run = int(input("\nWant to continue? (Yes = Input 1/false = Input 0) : "))

            elif ch == 3:
                run = False

            else:
                print("Invalid Choice!!!")


    if __name__ == '__main__':
        main()




elif choice == 4:
    from prettytable import PrettyTable
    import matplotlib.pyplot as plt
    def sortFunc(lst_process, lst_names):
        copy_names = lst_names[:]
        copy_lst = lst_process[:]
        new_lst = [[0, 0, 0]]   # Initializing CPU
        minVal = min(copy_lst, key = lambda x : x[0])   # To Find Out if the Processes Arrive at 0 or not
        remVal = minVal[0]
        currentTime = remVal

        ready_que = []

        #print(new_lst)
        while copy_lst:
            temp = []
            temp_names = []
            #print(currentTime)

            for val, name in zip(copy_lst, copy_names):
                at, bt, pt = val
                if at <= currentTime:
                    temp.append([at, bt, pt])
                    temp_names.append(name)
            #print(temp)

            minVal = min(temp, key = lambda x: -x[2])
            minVal_index = copy_lst.index(minVal)
            if minVal[1] != 0:
                new_lst += [[minVal[0], minVal[1]-1], minVal[2]]
                ready_que.append(copy_names[minVal_index])
                copy_lst[minVal_index][1] -= 1
                currentTime += 1
            else:
                copy_lst.pop(minVal_index)
                copy_names.pop(minVal_index)
            #print(new_lst)

        new_lst.pop(0)
        return new_lst, ready_que

    num = int(input("Please Enter Number of Processes: "))
    # process_lst = [[2, 6], [5, 2], [1, 8], [0, 3], [4, 4]]
    arrival_time_lst = []
    burst_time_lst = []
    priority_lst = []
    process_names = []

    for i in range(num):
        arrival_time = int(input(f"Please Input Arrival time for P{i+1}: "))
        burst_time = int(input(f"Please Input Burst Time for P{i+1}: "))
        priority = int(input(f"Please Input Priority Of P{i+1}: "))
        process_names.append(f"P{i+1}")
        arrival_time_lst.append(arrival_time)
        burst_time_lst.append(burst_time)
        priority_lst.append(priority)

    process_lst = list(zip(arrival_time_lst, burst_time_lst, priority_lst))
    temp_process_lst = [list(i) for i in process_lst]

    sorted_process_lst, new_process_names = sortFunc(temp_process_lst, process_names)

    print("Order of Execution:", new_process_names)

    new_process_lst = []
    average_WT = 0
    average_TAT = 0

    for process_name, process in zip(process_names, process_lst):
        for time, executed_process in enumerate(new_process_names):
            if process_name == executed_process:
                completion_time = time + 1       
        TAT = completion_time - process[0]
        average_WT += TAT - process[1]
        average_TAT += TAT
        new_process_lst.append([process_name, process[0], process[1], completion_time, TAT, TAT - process[1]])

    pt = PrettyTable()
    pt.field_names = ["Process", "Arrival Time", "Burst Time", "Completion Time", "TAT", "WT"]
    pt.add_rows(new_process_lst)
    print(pt)
    print(f"Average Waiting Time: {average_WT/num}")
    print(f"Average Turn Around Time: {average_TAT/num}")
    fig, ax = plt.subplots(figsize=(8, 3))
    
    for i, process in enumerate(new_process_lst):
        process_name = process[0]
        start_time = process[1]
        duration = process[4]
        ax.broken_barh([(start_time, duration)], (10 * i, 9), facecolors="tab:blue", edgecolor='black')
        ax.text(start_time + duration / 2, 10 * i + 4.5, process_name, ha="center", va="center")
    ax.set_xlim(0, max([process[3] for process in new_process_lst]) + 2)
    ax.set_ylim(0, 10 * len(new_process_lst))
    ax.set_xlabel("Time")
    ax.set_yticks([])
    ax.set_title("Gantt Chart")
    plt.show()


elif choice == 6:
    from prettytable import PrettyTable
    import matplotlib.pyplot as plt
    def sortFunc(lst):
        copy_lst = lst[:]
        new_lst = [[0, 0]]   # Initializing CPU
        minVal = min(copy_lst, key=lambda x: x[0])   # To Find Out if the Processes Arrive at 0 or not
        remVal = minVal[0]

        tempFunc = lambda x: x[1]

        while copy_lst:
            temp = []
            currentTime = sum(map(tempFunc, new_lst)) + remVal

            for index, val in enumerate(copy_lst):
                at, bt = val
                if at <= currentTime:
                    temp.append([at, bt])

            minVal = min(temp, key=tempFunc)
            new_lst += [minVal]
            copy_lst.pop(copy_lst.index(minVal))

        new_lst.pop(0)
        return new_lst

    num = int(input("Please Enter Number of Processes: "))
    process_lst = []
    process_names = []
    average_WT = 0
    average_TAT = 0

    for i in range(num):
        arrival_time = int(input(f"Please Input Arrival time for P{i+1}: "))
        burst_time = int(input(f"Please Input Burst Time for P{i+1}: "))
        process_names.append(f"P{i+1}")
        process_lst.append([arrival_time, burst_time])

    sorted_process_lst = sortFunc(process_lst)
    for i, val in enumerate(sorted_process_lst):
        idx = process_lst.index(val)
        sorted_process_lst[i].insert(0, process_names[idx])

    new_process_lst = []
    gantt_chart = []
    current_time = 0

    for i, val in enumerate(sorted_process_lst):
        pno, arrival, burst = val
        if current_time < arrival:
            current_time = arrival
        start_time = current_time
        completion_time = current_time + burst
        TAT = completion_time - arrival
        WT = TAT - burst
        average_WT += WT
        average_TAT += TAT
        new_process_lst.append([pno, arrival, burst, completion_time, TAT, WT])
        gantt_chart.append([pno, start_time, completion_time])
        current_time = completion_time

    pt = PrettyTable()
    pt.field_names = ["Process", "Arrival Time", "Burst Time", "Completion Time", "TAT", "WT"]
    pt.add_rows(new_process_lst)
    print(pt)
    print(f"Average Waiting Time: {average_WT / num}")
    print(f"Average Turn Around Time: {average_TAT / num}")

    # Gantt Chart Generation
    # Generate Gantt chart
    fig, ax = plt.subplots(figsize=(8, 3))
    for process in gantt_chart:
        process_name = process[0]
        start_time = process[1]
        end_time = process[2]
        duration = end_time - start_time
        ax.broken_barh([(start_time, duration)], (10, 9), facecolors="tab:blue", edgecolor='black')
        ax.text(start_time + duration / 2, 10 + 4.5, process_name, ha="center", va="center")
    ax.set_xlim(0, max([process[2] for process in gantt_chart]) + 2)
    ax.set_ylim(0, 20)
    ax.set_xlabel("Time")
    ax.set_yticks([])
    ax.set_title("Gantt Chart")
    plt.show()


elif choice == 7:
    from prettytable import PrettyTable
    import matplotlib.pyplot as plt

    def sortFunc(lst_process, lst_names):
        copy_names = lst_names[:]
        copy_lst = lst_process[:]
        new_lst = [[0, 0]]   # Initializing CPU
        minVal = min(copy_lst, key=lambda x: x[0])   # To Find Out if the Processes Arrive at 0 or not
        remVal = minVal[0]
        currentTime = remVal

        tempFunc = lambda x: x[1]

        ready_que = []

        #print(new_lst)
        while copy_lst:
            temp = []
            temp_names = []
            #print(currentTime)

            for val, name in zip(copy_lst, copy_names):
                at, bt = val
                if at <= currentTime:
                    temp.append([at, bt])
                    temp_names.append(name)
            #print(temp)

            minVal = min(temp, key=tempFunc)
            minVal_index = copy_lst.index(minVal)
            if minVal[1] != 0:
                new_lst += [[minVal[0], minVal[1]-1]]
                ready_que.append(copy_names[minVal_index])
                copy_lst[minVal_index][1] -= 1
                currentTime += 1
            else:
                copy_lst.pop(minVal_index)
                copy_names.pop(minVal_index)
            #print(new_lst)

        new_lst.pop(0)
        return new_lst, ready_que

    num = int(input("Please Enter Number of Processes: "))
    # process_lst = [[2, 6], [5, 2], [1, 8], [0, 3], [4, 4]]
    arrival_time_lst = []
    burst_time_lst = []
    process_names = []

    for i in range(num):
        arrival_time = int(input(f"Please Input Arrival time for P{i+1}: "))
        burst_time = int(input(f"Please Input Burst Time for P{i+1}: "))
        process_names.append(f"P{i+1}")
        arrival_time_lst.append(arrival_time)
        burst_time_lst.append(burst_time)

    process_lst = list(zip(arrival_time_lst, burst_time_lst))
    temp_process_lst = [list(i) for i in process_lst]

    sorted_process_lst, new_process_names = sortFunc(temp_process_lst, process_names)

    print("Order of execution:", new_process_names)

    new_process_lst = []
    average_WT = 0
    average_TAT = 0

    for process_name, process in zip(process_names, process_lst):
        for time, executed_process in enumerate(new_process_names):
            if process_name == executed_process:
                completion_time = time + 1       
        TAT = completion_time - process[0]
        average_WT += TAT - process[1]
        average_TAT += TAT
        new_process_lst.append([process_name, process[0], process[1], completion_time, TAT, TAT - process[1]])

    pt = PrettyTable()
    pt.field_names = ["Process", "Arrival Time", "Burst Time", "Completion Time", "TAT", "WT"]
    pt.add_rows(new_process_lst)
    print(pt)
    print(f"Average Waiting Time: {average_WT/num}")
    print(f"Average Turn Around Time: {average_TAT/num}")
    
    # Generate Gantt chart
    fig, ax = plt.subplots(figsize=(8, 3))
    for i, process_name in enumerate(new_process_names):
        start_time = i
        end_time = i + 1
        duration = end_time - start_time
        ax.broken_barh([(start_time, duration)], (10 * i, 9), facecolors="tab:blue", edgecolor='black')
        ax.text(start_time + duration / 2, 10 * i + 4.5, process_name, ha="center", va="center")
    ax.set_xlim(0, len(new_process_names) + 2)
    ax.set_ylim(0, 10 * len(new_process_names))
    ax.set_xlabel("Time")
    ax.set_yticks([])
    ax.set_title("Gantt Chart")
    plt.show()

else:
    print("Invalid choice. Exiting...")


