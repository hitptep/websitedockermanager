import os
import subprocess

def kill_process(port):
    pid = get_process_pid(port)
    if pid:
        try:
            subprocess.run(['kill', '-9', pid])
            print(f'Process with PID {pid} on port {port} has been killed')
        except Exception as e:
            print(f'Failed to kill process with PID {pid} on port {port}: {e}')

def get_process_pid(port):
    try:
        lsof_output = subprocess.check_output(['lsof', '-t', f':{port}'], text=True)
        return lsof_output.strip()
    except subprocess.CalledProcessError:
        print(f'No process is listening on port {port}')
        return None

if __name__ == '__main__':
    port = input('Enter the port number to kill the process on: ')
    kill_process(port)
