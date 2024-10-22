import serial
import tkinter as tk
from tkinter import scrolledtext

# initialize serial COM
ser_com = serial.Serial('COM8', 9600, timeout=1)

# create a window for COM
root_com = tk.Tk()
root_com.title("LoRa Communication GUI")

log_area_com = scrolledtext.ScrolledText(root_com, width=50, height=15)
log_area_com.pack()

entry_com = tk.Entry(root_com, width=50)
entry_com.pack()

def send_message_com():
    message = entry_com.get()
    if message:
        ser_com.write(message.encode('utf-8'))
        log_area_com.insert(tk.END, f"{message}\n")
        entry_com.delete(0, tk.END)

def read_from_serial_com():
    if ser_com.in_waiting:
        try:
            received_data = ser_com.readline().decode('utf-8').strip()
            log_area_com.insert(tk.END, f"{received_data}\n")
        except:
            pass
    root_com.after(100, read_from_serial_com)

send_button_com = tk.Button(root_com, text="Send", command=send_message_com)
send_button_com.pack()

# start reading data from COM
read_from_serial_com()

# start the main loop
root_com.mainloop()
