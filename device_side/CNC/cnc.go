package main


import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
)

func handleServerResponse(conn net.Conn) {
	reader := bufio.NewReader(conn)
	for {
		response, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading from server:", err)
			return
		}

		response = strings.TrimSpace(response)
		fmt.Println("Received from server:", response)

		// Perform actions based on server response (assuming it's a number)
		number, err := strconv.Atoi(response)
		if err == nil {
			switch number {
			case 1:
				fmt.Println("Performing action for number 1...")
				// Add your code for action based on number 1
			case 2:
				fmt.Println("Performing action for number 2...")
				// Add your code for action based on number 2
			default:
				fmt.Println("Unknown number received from server.")
			}
		}
	}
}

func main() {
	serverAddr := "192.168.1.97:8888" // Replace with your server IP and port
	conn, err := net.Dial("tcp", serverAddr)
	if err != nil {
		fmt.Println("Error connecting to server:", err)
		return
	}
	defer conn.Close()

	go handleServerResponse(conn)

	for {
		// Read user input
		reader := bufio.NewReader(os.Stdin)
		fmt.Print("Enter a number to send to the server: ")
		input, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading input:", err)
			return
		}

		// Send input to server
		_, err = conn.Write([]byte(input))
		if err != nil {
			fmt.Println("Error sending data to server:", err)
			return
		}
	}
}
