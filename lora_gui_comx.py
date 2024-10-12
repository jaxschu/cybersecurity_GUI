import serial
import tkinter as tk
from tkinter import scrolledtext

# initialize serial COM6
ser_com6 = serial.Serial('COM6', 9600, timeout=1)

# create a window for COM6
root_com6 = tk.Tk()
root_com6.title("LoRa Communication GUI COM6")

log_area_com6 = scrolledtext.ScrolledText(root_com6, width=50, height=15)
log_area_com6.pack()

entry_com6 = tk.Entry(root_com6, width=50)
entry_com6.pack()

def send_message_com6():
    message = entry_com6.get()
    if message:
        ser_com6.write(message.encode('utf-8'))
        log_area_com6.insert(tk.END, f"COM6 Sent: {message}\n")
        entry_com6.delete(0, tk.END)

def read_from_serial_com6():
    if ser_com6.in_waiting:
        try:
            received_data = ser_com6.readline().decode('utf-8').strip()
            log_area_com6.insert(tk.END, f"COM6 Received: {received_data}\n")
        except:
            pass
    root_com6.after(100, read_from_serial_com6)

send_button_com6 = tk.Button(root_com6, text="Send", command=send_message_com6)
send_button_com6.pack()

# start reading data from COM6
read_from_serial_com6()

# start the main loop
root_com6.mainloop()
