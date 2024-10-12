import serial
import tkinter as tk
from tkinter import scrolledtext

# init serial port
ser = serial.Serial('COM4', 9600, timeout=1)

# create a GUI window
root = tk.Tk()
root.title("LoRa Communication GUI")

# display area for log
log_area = scrolledtext.ScrolledText(root, width=50, height=15)
log_area.pack()

# send message entry
entry = tk.Entry(root, width=50)
entry.pack()

def send_message():
    # get message from entry and send it to serial port
    message = entry.get()
    if message:
        ser.write(message.encode('utf-8'))
        log_area.insert(tk.END, f"Sent: {message}\n")
        entry.delete(0, tk.END)

def read_from_serial():
    # get data from serial port and display it in log area
    if ser.in_waiting:
        try:
            received_data = ser.readline().decode('utf-8').strip()
            log_area.insert(tk.END, f"Received: {received_data}\n")
        except:
            pass
    root.after(100, read_from_serial)

# sned button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

# begin to read from serial port
read_from_serial()

# begin the GUI loop
root.mainloop()