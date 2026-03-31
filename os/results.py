import pandas as pd
import matplotlib.pyplot as plt

def plot_scheduler_performance():
    # 1. Read the CSV file
    try:
        df = pd.read_csv('results.csv')
    except FileNotFoundError:
        print("Error: 'results.csv' not found. Run your Go program first!")
        return

    # 2. Setup the Plotting Area
    # We will use a "Grouped Bar Chart" to compare Waiting vs Turnaround time
    plt.figure(figsize=(10, 6))

    # 3. Create the Bar Chart
    # We plot 'Algorithm' on X-axis, and the metrics on Y-axis
    x_positions = range(len(df['Algorithm']))
    width = 0.35  # Width of the bars

    plt.bar([p - width/2 for p in x_positions], df['AvgWaiting'], width, label='Avg Waiting Time', color='#4c72b0')
    plt.bar([p + width/2 for p in x_positions], df['AvgTurnaround'], width, label='Avg Turnaround Time', color='#dd8452')

    # 4. Styling the Chart
    plt.xlabel('Scheduling Algorithm', fontweight='bold')
    plt.ylabel('Time Units', fontweight='bold')
    plt.title('CPU Scheduling Analysis: FCFS vs SJF', fontsize=14)
    
    # Set the X-axis labels to be the algorithm names
    plt.xticks(x_positions, df['Algorithm'])
    
    # Add a legend so we know which color is which
    plt.legend()
    
    # Add grid lines for easier reading
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 5. Display
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_scheduler_performance()