import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading

def scan_ports():
    target = entry.get()
    if not target:
        messagebox.showerror("Error", "Please enter a target host/IP.")
        return

    port_names = {
        20: "FTP", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB", 3389: "RDP"
    }

    try:
        results_display.delete(1.0, tk.END)
        results_display.insert(tk.END, f"Scanning ports on {target}...\n")
        open_ports = []
        for port in range(1, 1025):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if not s.connect_ex((target, port)):
                    port_name = port_names.get(port, "Unknown Service")
                    results_display.insert(tk.END, f"Port {port} is open ({port_name})\n")
                    open_ports.append(port)
        if open_ports:
            results_display.insert(tk.END, "\nDevice might not be secure! Open ports found:\n")
        else:
            results_display.insert(tk.END, "\nDevice appears secure! No open ports found.\n")
        results_display.insert(tk.END, "\nEnd Of Action.")
    except Exception as e:
        results_display.insert(tk.END, f"Error: {str(e)}\n")

def start_scan():
    threading.Thread(target=scan_ports, daemon=True).start()

def clear_entry():
    entry.delete(0, tk.END)

# Create main application window
app = tk.Tk()
app.title("Port Scanner")
app.geometry("800x450")
app.resizable(False, False)

# Input field
input_frame = tk.Frame(app)
input_frame.pack(pady=20)

entry_label = tk.Label(input_frame, text="Target Host/IP:")
entry_label.grid(row=0, column=0, padx=10, pady=10)

entry = tk.Entry(input_frame, width=40)
entry.grid(row=0, column=1, padx=10, pady=10)

scan_button = tk.Button(input_frame, text="Scan Ports", command=start_scan)
scan_button.grid(row=0, column=2, padx=10, pady=10)

clear_button = tk.Button(input_frame, text="Clear Entry", command=clear_entry)
clear_button.grid(row=0, column=3, padx=10, pady=10)

# Results display
results_frame = tk.Frame(app)
results_frame.pack(padx=20, pady=20)
results_display = scrolledtext.ScrolledText(results_frame, width=100, height=15)
results_display.pack()

# Signature
signature = tk.Label(app, text="Made in Antwerp by Runaque", font=("Arial", 10), fg="slategrey")
signature.pack(side="bottom", pady=10)

# Run the app
app.mainloop()
