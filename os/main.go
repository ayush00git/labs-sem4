package main

import (
	"fmt"
	"math"
)

// --- 1. DATA STRUCTURES ---

type Process struct {
	ID        int
	Arrival   int
	Burst     int
	// Dynamic State
	Remaining int
	StartTime int
	Finish    int
	WaitTime  int
	TurnTime  int
}

// The Interface ensuring both algos work with the same simulator
type Scheduler interface {
	Name() string
	Select(queue []*Process, current *Process) int
}

// --- 2. ALGORITHMS ---

// A. First-Come, First-Served (FCFS)
type FCFS struct{}

func (f FCFS) Name() string { return "FCFS" }
func (f FCFS) Select(queue []*Process, current *Process) int {
	// Non-Preemptive: If someone is running, don't interrupt
	if current != nil {
		return -1
	}
	// Simple: Pick the first one in the queue
	if len(queue) > 0 {
		return 0
	}
	return -1
}

// B. Shortest Job First - Non-Preemptive (SJF-NP)
type SJF_NP struct{}

func (s SJF_NP) Name() string { return "SJF-NP" }
func (s SJF_NP) Select(queue []*Process, current *Process) int {
	// Non-Preemptive: If someone is running, don't interrupt
	if current != nil {
		return -1
	}
	if len(queue) == 0 {
		return -1
	}

	// Logic: Find the process with the smallest Burst time
	bestIdx := -1
	minBurst := math.MaxInt32

	for i, p := range queue {
		if p.Burst < minBurst {
			minBurst = p.Burst
			bestIdx = i
		}
	}
	return bestIdx
}

// --- 3. SIMULATION ENGINE ---

func RunSimulator(inputData []Process, sched Scheduler) {
	// Deep copy data to keep tests isolated
	var procs []*Process
	for _, p := range inputData {
		temp := p
		temp.Remaining = p.Burst
		temp.StartTime = -1
		procs = append(procs, &temp)
	}

	time := 0
	completed := 0
	var queue []*Process
	var current *Process

	for completed < len(procs) {
		// 1. Check Arrivals
		for _, p := range procs {
			if p.Arrival == time {
				queue = append(queue, p)
			}
		}

		// 2. Scheduler Decision
		idx := sched.Select(queue, current)
		if idx != -1 {
			current = queue[idx]
			queue = append(queue[:idx], queue[idx+1:]...)
		}

		// 3. Execution
		if current != nil {
			if current.StartTime == -1 {
				current.StartTime = time
			}
			current.Remaining--

			if current.Remaining == 0 {
				current.Finish = time + 1
				current.TurnTime = current.Finish - current.Arrival
				current.WaitTime = current.TurnTime - current.Burst
				completed++
				current = nil
			}
		}
		time++
	}

	// 4. Output Results in CSV Format
	var totalWait, totalTurn float64
	for _, p := range procs {
		totalWait += float64(p.WaitTime)
		totalTurn += float64(p.TurnTime)
	}
	n := float64(len(procs))
	throughput := n / float64(time)
    
    // IMPORTANT: precise CSV formatting
	fmt.Printf("%s,%.2f,%.2f,%.4f\n", sched.Name(), totalWait/n, totalTurn/n, throughput)
}

// --- 4. MAIN ---

func main() {
	// Sample Data
	data := []Process{
		{ID: 1, Arrival: 0, Burst: 8},
		{ID: 2, Arrival: 1, Burst: 4},
		{ID: 3, Arrival: 2, Burst: 9},
		{ID: 4, Arrival: 3, Burst: 5},
	}

    // Print the CSV Header ONCE
	fmt.Println("Algorithm,AvgWaiting,AvgTurnaround,Throughput")

	RunSimulator(data, FCFS{})
	RunSimulator(data, SJF_NP{})
}