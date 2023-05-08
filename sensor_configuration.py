import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

import can
import cantools

def send_can_message():
    try:
        channel = entry_channel.get()
        bitrate = int(entry_bitrate.get())

        bus = can.interface.Bus(channel=channel, bustype='pcan', bitrate=bitrate)

        # Get the integer value corresponding to the selected text enumeration
        selected_int_value2 = [key for key, value in int_value2_options.items() if value == entry_int_value2.get()][0]
        entered_int_value3 = int(int_value_3.get(), 8)
        entered_int_value4 = int(int_value_4.get(), 8)
        entered_int_value5 = int(int_value_5.get(), 8)
        entered_int_value6 = int(int_value_6.get(), 8)
        entered_int_value7 = int(int_value_7.get(), 8)

        int_values = [
            0x6,
            0x66,
            selected_int_value2,
            entered_int_value3,
            entered_int_value4,
            entered_int_value5,
            entered_int_value6,
            entered_int_value7,
        ]

        data = bytearray()

        for int_value in int_values:
            data.extend(int_value.to_bytes(1, byteorder='big'))

        arbitration_id = int(entry_can_id.get(), 16)
        can_message = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)
        bus.send(can_message)

        messagebox.showinfo("Success", "CAN message sent successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))



# GUI
root = tk.Tk()
root.title("PCAN-USB Obsidian Group Sensor Config")
frame = tk.Frame(root, padx=60, pady=60)
frame.grid()

# Load the image
logo_image = Image.open("logo.png")

# Resize the image (optional)
logo_image = logo_image.resize((400, 400), Image.ANTIALIAS)

# Create a PhotoImage object
logo_photo = ImageTk.PhotoImage(logo_image)

# Create a Label widget with the PhotoImage object
logo_label = tk.Label(frame, image=logo_photo)

# Add the Label widget to the GUI
logo_label.grid(row=0, columnspan=2, pady=10)


label_channel = tk.Label(frame, text="Channel (interface):")
label_channel.grid(row=1, column=0)
entry_channel = tk.Entry(frame)
entry_channel.grid(row=1, column=1)
entry_channel.insert(0, "PCAN_USBBUS1")

label_bitrate = tk.Label(frame, text="Bitrate (bps):")
label_bitrate.grid(row=2, column=0)
entry_bitrate = tk.Entry(frame)
entry_bitrate.grid(row=2, column=1)
entry_bitrate.insert(0, "1000000")

label_can_id = tk.Label(frame, text="CAN ID (hex):")
label_can_id.grid(row=3, column=0)
entry_can_id = tk.Entry(frame)
entry_can_id.grid(row=3, column=1)
entry_can_id.insert(0, "6")

int_value2_options = {
    0x10: "Adaptive Filtering (On / Off Toggle)",
    0x11: "Accel / Gyro Filtering (On / Off Toggle + Filter Parameters)",
    0x12: "AHRS Control (On / Off Toggle)",
    0x13: "Adaptive Filtering Parameters (Filter Parameters)",
    0x14: "Antenna Lever Arm Translation (Translation Parameters)",
    0x20: "Transmission Rate Control (Rate Parameters)",
    0x21: "CAN Baud Rate Control (Rate Parameters)",
    0x30: "GPS Simulation Option (Simulation Parameters)",
    0x40: "Dead Reckoning (On / Off Toggle)",
    0x66: "Write Settings To Memory (On / Off Toggle)",
    0x67: "Write Defaults To Memory (On / Off Toggle)"
}

label_int_value2 = tk.Label(frame, text="Control Parameter (byte 2):", width=30)
label_int_value2.grid(row=4, column=0)

entry_int_value2 = ttk.Combobox(frame, values=list(int_value2_options.values()), state='readonly', width=60)
entry_int_value2.grid(row=4, column=1)
entry_int_value2.set(list(int_value2_options.values())[0])  # Set the default value

int_value_3 = tk.Label(frame, text="User Input Parameter (byte 3 (hex)):", width=30)
int_value_3.grid(row=5, column=0)
int_value_3 = tk.Entry(frame)
int_value_3.grid(row=5, column=1)
int_value_3.insert(0, "0")

int_value_4 = tk.Label(frame, text="User Input Parameter (byte 4 (hex)):", width=30)
int_value_4.grid(row=6, column=0)
int_value_4 = tk.Entry(frame)
int_value_4.grid(row=6, column=1)
int_value_4.insert(0, "0")

int_value_5 = tk.Label(frame, text="User Input Parameter (byte 5 (hex)):", width=30)
int_value_5.grid(row=7, column=0)
int_value_5 = tk.Entry(frame)
int_value_5.grid(row=7, column=1)
int_value_5.insert(0, "0")

int_value_6 = tk.Label(frame, text="User Input Parameter (byte 6 (hex)):", width=30)
int_value_6.grid(row=8, column=0)
int_value_6 = tk.Entry(frame)
int_value_6.grid(row=8, column=1)
int_value_6.insert(0, "0")

int_value_7 = tk.Label(frame, text="User Input Parameter (byte 7 (hex)):", width=30)
int_value_7.grid(row=9, column=0)
int_value_7 = tk.Entry(frame)
int_value_7.grid(row=9, column=1)
int_value_7.insert(0, "0")

button_send = tk.Button(frame, text="Send", command=send_can_message)
button_send.grid(row=20, columnspan=8, pady=10)

root.mainloop()
