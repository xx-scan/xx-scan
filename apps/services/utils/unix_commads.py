import paramiko

def sshclient_execmd(hostname="192.168.2.9",
                     port=22,
                     username="root",
                     password="123456",
                     execmd="yglzgat"):
    import os
    DIR_NAME = os.path.dirname(os.path.abspath(__file__))
    paramiko.util.log_to_file(os.path.join(DIR_NAME, "paramiko.log"))
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=hostname, port=port, username=username, password=password, timeout=20)
    stdin, stdout, stderr = s.exec_command(execmd)
    # stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
    outstr = stdout.read()
    s.close()
    return outstr

# print(sshclient_execmd(execmd="ip addr").decode("utf-8").split("\n"))
