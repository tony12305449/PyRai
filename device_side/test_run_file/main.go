package main

import (
	"fmt"
	"runtime"
)

func main() {
	// Set a memory limit for the program (in bytes)
	const memoryLimit = 10 // Change this value as needed

	// Set the memory limit for the Go runtime
	runtime.GOMAXPROCS(1) // Limit to one CPU core for this example
	runtime.GC()          // Run the garbage collector to free any unused memory
	runtime.MemProfileRate = 0

	// Allocate a large slice to potentially consume memory
	largeSlice := make([]int, 0, memoryLimit)

	// Fill the slice with data (optional)
	for i := 0; i < memoryLimit; i++ {
		largeSlice = append(largeSlice, i)
	}

	// Force a garbage collection to free unused memory
	runtime.GC()

	// Check the memory usage
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	fmt.Printf("Allocated memory: %d bytes\n", m.Alloc)
}
