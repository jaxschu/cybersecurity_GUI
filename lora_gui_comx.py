import serial
import tkinter as tk
from tkinter import scrolledtext



# initialize serial COM4
ser_com4 = serial.Serial('COM4', 9600, timeout=1)

# create a window for COM4
root_com4 = tk.Tk()
root_com4.title("LoRa Communication GUI COM4")

log_area_com4 = scrolledtext.ScrolledText(root_com4, width=50, height=15)
log_area_com4.pack()

entry_com4 = tk.Entry(root_com4, width=50)
entry_com4.pack()

def send_message_com4():
    message = entry_com4.get()
    if message:
        ser_com4.write(message.encode('utf-8'))
        log_area_com4.insert(tk.END, f"COM4 Sent: {message}\n")
        entry_com4.delete(0, tk.END)

def read_from_serial_com4():
    if ser_com4.in_waiting:
        try:
            received_data = ser_com4.readline().decode('utf-8').strip()
            log_area_com4.insert(tk.END, f"COM4 Received: {received_data}\n")
        except:
            pass
    root_com4.after(100, read_from_serial_com4)

send_button_com4 = tk.Button(root_com4, text="Send", command=send_message_com4)
send_button_com4.pack()

# start reading data from COM4
read_from_serial_com4()

# start the main loop
root_com4.mainloop()
