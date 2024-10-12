import serial
import tkinter as tk
from tkinter import scrolledtext

# initialize serial COM3
ser_com3 = serial.Serial('COM3', 9600, timeout=1)

# create a window for COM3
root_com3 = tk.Tk()
root_com3.title("LoRa Communication GUI COM3")

log_area_com3 = scrolledtext.ScrolledText(root_com3, width=50, height=15)
log_area_com3.pack()

entry_com3 = tk.Entry(root_com3, width=50)
entry_com3.pack()

def send_message_com3():
    message = entry_com3.get()
    if message:
        ser_com3.write(message.encode('utf-8'))
        log_area_com3.insert(tk.END, f"COM3 Sent: {message}\n")
        entry_com3.delete(0, tk.END)

def read_from_serial_com3():
    if ser_com3.in_waiting:
        try:
            received_data = ser_com3.readline().decode('utf-8').strip()
            log_area_com3.insert(tk.END, f"COM3 Received: {received_data}\n")
        except:
            pass
    root_com3.after(100, read_from_serial_com3)

send_button_com3 = tk.Button(root_com3, text="Send", command=send_message_com3)
send_button_com3.pack()

# start reading data from COM3
read_from_serial_com3()

# start the main loop
root_com3.mainloop()
