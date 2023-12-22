import paramiko
import subprocess
import pytest
import sys
import time
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

@pytest.fixture(scope="function")
def client(server):
    with server as ssh:
        return subprocess.run(["iperf3", "-c", '192.168.0.136', "--json"], capture_output=True, text=True)

@pytest.fixture(scope="function")
def server():
    with paramiko.SSHClient() as ssh:
        print("Done SSH connection")
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname='192.168.0.136', username="polinast", password="2108")
            print("Connected to iperf server")

            stdin, stdout, stderr = ssh.exec_command("iperf3 -s -1 &")

            time.sleep(2)
            yield ssh

        except paramiko.AuthenticationException:
            print("Connection failed")
            sys.exit(1)
