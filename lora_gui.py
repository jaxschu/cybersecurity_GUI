import serial
import tkinter as tk
from tkinter import scrolledtext
import threading

# 初始化COM3和COM4的串口
ser_com3 = serial.Serial('COM3', 9600, timeout=1)
ser_com4 = serial.Serial('COM5', 9600, timeout=1)

# 创建一个窗口，用于串口COM3
def create_gui_com3():
    root_com3 = tk.Tk()
    root_com3.title("LoRa Communication GUI")

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

    # 开始读取COM3的数据
    read_from_serial_com3()

    root_com3.mainloop()

# 创建一个窗口，用于串口COM4
def create_gui_com4():
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

    # 开始读取COM4的数据
    read_from_serial_com4()

    root_com4.mainloop()

# 使用线程来分别运行两个窗口
thread_com3 = threading.Thread(target=create_gui_com3)
thread_com4 = threading.Thread(target=create_gui_com4)

# 启动两个线程
thread_com3.start()
thread_com4.start()

# 确保主线程等待两个GUI窗口关闭
thread_com3.join()
thread_com4.join()
