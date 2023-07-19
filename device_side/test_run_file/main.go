package main

import(
	"fmt"
	"os/exec"
)


func main(){
	user:="admin"
	password:="password"
	ip:="192.168.1.181"
	port:="23"
	fmt.Println("execute this file")
	cmd:=exec.Command("./loader",user,password,ip,port)
	cmd.Run()
	fmt.Println("finish")
}