package main

import (
	"bufio"
	"fmt"
	"net"
	
)

func startClient() {
	host := "192.168.6.128"
	port := 12345

	conn, err := net.Dial("tcp", fmt.Sprintf("%s:%d", host, port))
	if err != nil {
		fmt.Println("Error connecting to C&C Server:", err)
		return
	}
	defer conn.Close()

	fmt.Println("Connected to C&C Server.")

	reader := bufio.NewReader(conn)

	for {

		command, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading command:", err)
			return
		}

		command = command[:len(command)-1] 

		if len(command) > 0 {
			fmt.Println("Received command:", command)

			response := "Command executed successfully!\n"
			conn.Write([]byte(response))
		}
	}
}

func main() {
	startClient()
}
