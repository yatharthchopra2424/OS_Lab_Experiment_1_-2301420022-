import os
import time
import sys

# Task 1: Create N child processes [cite: 35]
def task1(n=3):
    """Creates n child processes, each printing its PID and parent PID."""
    print("--- Running Task 1: Process Creation ---")
    pids = []
    for i in range(n):
        pid = os.fork()
        if pid == 0:  # This is the child process
            print(f"Child (PID: {os.getpid()}) created by Parent (PPID: {os.getppid()}). Message: Hello from child {i+1}")
            os._exit(0) # Child exits after printing
        else: # This is the parent process
            pids.append(pid)
    
    # Parent waits for all children to finish [cite: 36]
    for pid in pids:
        os.waitpid(pid, 0)
    print("--- Task 1 Finished: Parent has waited for all children. ---\n")

# Task 2: Execute a command using execvp [cite: 38]
def task2():
    """Creates a child process that executes a Linux command."""
    print("--- Running Task 2: Command Execution ---")
    pid = os.fork()
    if pid == 0:  # Child process
        print(f"Child (PID: {os.getpid()}) is executing the 'ls -l' command.")
        try:
            os.execvp("ls", ["ls", "-l"])
        except FileNotFoundError:
            print("Error: Command not found.")
            os._exit(1)
    else:  # Parent process
        os.wait()
        print("--- Task 2 Finished: Child has executed the command. ---\n")

# Task 3: Simulate Zombie and Orphan Processes [cite: 40]
def zombie_process():
    """Creates a zombie process."""
    print("--- Running Task 3a: Zombie Process Simulation ---")
    pid = os.fork()
    if pid == 0:  # Child
        print(f"Zombie Child (PID: {os.getpid()}) created. It will exit immediately.")
        os._exit(0)
    else:  # Parent
        print(f"Parent (PID: {os.getpid()}) is sleeping for 10 seconds, not waiting.")
        time.sleep(10)
        # The parent doesn't call os.wait(), so the child becomes a zombie.
        print("Parent is done. The child should now be gone.")
        # We add a wait call here to clean up the zombie after demonstration
        os.wait() 
    print("--- Task 3a Finished. Check terminal output for 'ps' command. ---\n")

def orphan_process():
    """Creates an orphan process."""
    print("--- Running Task 3b: Orphan Process Simulation ---")
    pid = os.fork()
    if pid == 0:  # Child
        print(f"Child (PID: {os.getpid()}) is sleeping for 5 seconds.")
        time.sleep(5)
        # By the time the child wakes up, the original parent will be gone.
        # The child will be "adopted" by the 'init' process (PID 1).
        print(f"Child is awake. My PID is {os.getpid()}, and my Parent's PID is now {os.getppid()}.")
        os._exit(0)
    else:  # Parent
        print(f"Parent (PID: {os.getpid()}) is exiting immediately.")
        os._exit(0)

# Task 4: Inspect process information from /proc [cite: 43]
def inspect_process(pid):
    """Reads and prints details for a given PID from the /proc filesystem."""
    print(f"--- Running Task 4: Inspecting PID {pid} ---")
    try:
        # Read process name, state, and memory usage from /proc/[pid]/status
        with open(f"/proc/{pid}/status") as f:
            for line in f:
                if line.startswith("Name:") or line.startswith("State:") or line.startswith("VmSize:"):
                    print(line.strip())
        
        # Read the executable path
        exe_path = os.readlink(f"/proc/{pid}/exe")
        print(f"Executable Path: {exe_path}")

        # List open file descriptors
        fds = os.listdir(f"/proc/{pid}/fd")
        print(f"Open File Descriptors: {len(fds)} ({fds})")

    except (FileNotFoundError, PermissionError) as e:
        print(f"Could not inspect PID {pid}. Error: {e}")
    print("--- Task 4 Finished. ---\n")

# Task 5: Process prioritization with nice values [cite: 45]
def task5(n=3):
    """Demonstrates scheduler impact using different nice values."""
    print("--- Running Task 5: Process Prioritization ---")
    print("Starting CPU-intensive tasks with different priorities (lower nice value = higher priority).")
    
    for i in range(n):
        pid = os.fork()
        if pid == 0: # Child
            nice_val = i * 5 # Assign nice values 0, 5, 10
            os.nice(nice_val)
            
            # Simple CPU-intensive task
            print(f"Child (PID: {os.getpid()}, nice: {nice_val}) starting.")
            result = sum(j for j in range(30000000))
            print(f"Child (PID: {os.getpid()}, nice: {nice_val}) finished.")
            os._exit(0)

    # Parent waits for all children
    for _ in range(n):
        os.wait()
    print("--- Task 5 Finished. Observe the finishing order. ---\n")

# Main menu to run tasks
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 process_management.py <task_number>")
        print("Available tasks: 1, 2, 3a (zombie), 3b (orphan), 4, 5")
        return

    task = sys.argv[1]
    if task == '1':
        task1()
    elif task == '2':
        task2()
    elif task == '3a':
        print("--> To see the zombie, run this command in another terminal window while this script is sleeping: ")
        print("--> ps -el | grep defunct")
        zombie_process()
    elif task == '3b':
        orphan_process()
    elif task == '4':
        pid_to_inspect = input("Enter PID to inspect (you can use your own shell's PID, for example): ")
        try:
            inspect_process(int(pid_to_inspect))
        except ValueError:
            print("Invalid PID.")
    elif task == '5':
        task5()
    else:
        print("Invalid task number. Please choose from: 1, 2, 3a, 3b, 4, 5")

if __name__ == "__main__":
    main()
