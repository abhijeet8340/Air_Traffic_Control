import tkinter as tk
from tkinter import messagebox
import heapq  # For Dijkstra's algorithm


# Dijkstra's algorithm to find the shortest path
def dijkstra(graph, start, end):
    # Initialize the priority queue and distances dictionary
    queue = [(0, start)]  # (distance, node)
    distances = {start: 0}
    previous_nodes = {start: None}  

    while queue:
        current_distance, node = heapq.heappop(queue)

        if node == end:
            # Reconstruct the shortest path
            path = []
            while node is not None:
                path.append(node)
                node = previous_nodes[node]
            return path[::-1]  # Return reversed path

        for neighbor in graph.get(node, []):
            # All edges have the same weight of 1 (assuming unweighted graph)
            distance = current_distance + 1
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = node
                heapq.heappush(queue, (distance, neighbor))

    return None


# Function that will be called when the "Find Path" button is clicked
def find_path():
    airport_from = entry_from.get().strip()
    airport_to = entry_to.get().strip()

    # Check if the input fields are empty
    if not airport_from or not airport_to:
        messagebox.showerror("Error", "Please fill in both the departure and destination airports.")
        return

    # Check if the airports are recognized
    if airport_from not in airports:
        messagebox.showerror("Error", f"The departure airport '{airport_from}' is not recognized.")
        return
    if airport_to not in airports:
        messagebox.showerror("Error", f"The destination airport '{airport_to}' is not recognized.")
        return

    # Check if the departure and destination airports are the same
    if airport_from == airport_to:
        messagebox.showerror("Error", "The departure and destination airports cannot be the same.")
        return

    # Find the shortest path using Dijkstra's algorithm
    path = dijkstra(graph, airport_from, airport_to)

    if path:
        result_label.config(text=f"The shortest path from {airport_from} to {airport_to} is:\n{' -> '.join(path)}")
    else:
        result_label.config(text=f"Sorry, no path found from {airport_from} to {airport_to}.")

    clear_button.grid(row=7, column=0, columnspan=2, pady=10)  # Ensure clear button is displayed


# Function to clear the inputs and output
def clear_fields():
    entry_from.delete(0, tk.END)
    entry_to.delete(0, tk.END)
    result_label.config(text="")
    clear_button.grid_forget()  # Hide the clear button after clearing the fields


# Function to show all available airports
def show_airports():
    airports_list = "\n".join(airports)
    messagebox.showinfo("All Airports", f"The available airports are:\n\n{airports_list}")


# Function to show all routes
def show_routes():
    routes_list = "\n".join([f"{start}: {', '.join(neighbors)}" for start, neighbors in graph.items()])
    messagebox.showinfo("All Routes", f"The available routes are:\n\n{routes_list}")


# List of airports
airports = ["Amsterdam", "Athens", "Berlin", "Bucharest", "Budapest", "Dublin", "Geneva", "London", "Lisbon", "Madrid",
            "Oslo", "Paris", "Reykjavik", "Rome"]

# Graph representing direct flight connections between airports
graph = {
    "Amsterdam": ["London", "Paris", "Geneva"],
    "London": ["Amsterdam", "Berlin", "Dublin"],
    "Paris": ["Amsterdam", "Madrid", "Oslo"],
    "Madrid": ["Paris", "Lisbon"],
    "Lisbon": ["Madrid", "Reykjavik"],
    "Oslo": ["Paris", "Rome"],
    "Rome": ["Oslo", "Reykjavik", "London"],
    "Berlin": ["London", "Budapest"],
    "Dublin": ["London", "Reykjavik"],
    "Geneva": ["Amsterdam", "Bucharest"],
    "Bucharest": ["Geneva", "Athens"],
    "Budapest": ["Berlin", "Athens"],
    "Athens": ["Bucharest", "Budapest", "Berlin"],
    "Reykjavik": ["Lisbon", "Rome"]
}

# Create the main window
root = tk.Tk()
root.title("Air Traffic Control Planner")
# Set the background color of the window
root.configure(bg="Light pink")
root.geometry("600x600")
root.resizable(False, False)

# Center the window on the screen
window_width = 600
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Create frames for layout organization
frame = tk.Frame(root, padx=20, pady=20, bg="#f2f2f2")
frame.pack(padx=20, pady=20, expand=True)

# Instructions/Description Section
instructions_label = tk.Label(frame,
                              text="Welcome to the Air Traffic Planner!\nPlease enter a departure and destination airport to find the shortest flight route.",
                              font=("Helvetica", 14), bg="#f2f2f2", wraplength=550, justify="left")
instructions_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

# Title label with underline
title_label = tk.Label(frame, text="Air Traffic Planner", font=("Helvetica", 20, "bold"), bg="light blue")
title_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

# Departure airport label with underline
label_from = tk.Label(frame, text="Departure Airport:", font=("Helvetica", 14), bg="#f2f2f2")
label_from.grid(row=2, column=0, sticky="w", padx=(0, 10))

# Entry field for departure airport
entry_from = tk.Entry(frame, font=("Helvetica", 14), width=30, relief="solid", bd=2)
entry_from.grid(row=2, column=1)

# Destination airport label with underline
label_to = tk.Label(frame, text="Destination Airport:", font=("Helvetica", 14), bg="#f2f2f2")
label_to.grid(row=3, column=0, sticky="w", padx=(0, 10), pady=(10, 0))

# Entry field for destination airport
entry_to = tk.Entry(frame, font=("Helvetica", 14), width=30, relief="solid", bd=2)
entry_to.grid(row=3, column=1)

# Find Path Button
find_button = tk.Button(frame, text="Find Shortest Path", font=("Helvetica", 14), command=find_path, bg="lightblue",
                        relief="solid", bd=2)
find_button.grid(row=4, column=0, columnspan=2, pady=20)

# Show All Airports Button
show_airports_button = tk.Button(frame, text="Show All Airports", font=("Helvetica", 14), command=show_airports,
                                 bg="lightgreen", relief="solid", bd=2)
show_airports_button.grid(row=5, column=0, pady=10)

# Show All Routes Button
show_routes_button = tk.Button(frame, text="Show All Routes", font=("Helvetica", 14), command=show_routes,
                               bg="lightyellow", relief="solid", bd=2)
show_routes_button.grid(row=5, column=1, pady=10)

# Result Label to show the output
result_label = tk.Label(frame, text="", font=("Helvetica", 14), wraplength=400, justify="left", bg="#f2f2f2")
result_label.grid(row=6, column=0, columnspan=2, pady=10)

# Clear Button to reset the fields
clear_button = tk.Button(frame, text="Clear Fields", font=("Helvetica", 14), command=clear_fields, bg="lightcoral",
                         relief="solid", bd=2)

# Start the Tkinter event loop
root.mainloop()