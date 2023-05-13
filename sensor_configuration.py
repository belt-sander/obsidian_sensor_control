import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

import can
import cantools


entry_int_values = []


def add_int_value_entry():
    """
    Unused right now. Will be used for "Expert Mode"
    """
    label = tk.Label(frame, text=f"User Input Parameter (byte {len(entry_int_values) + 3} (hex)):", width=30)
    label.grid(row=len(entry_int_values) + 5, column=0)
    entry = tk.Entry(frame)
    entry.grid(row=len(entry_int_values) + 5, column=1)
    entry.insert(0, "0")
    entry_int_values.append(entry)


def clear_int_value_entries():
    for entry in entry_int_values:
        entry.grid_forget()
    entry_int_values.clear()


def update_gui_options(*args):
    selected_option = int_value2_var.get()

    clear_int_value_entries()

    if selected_option == "Adaptive Filtering (On / Off Toggle)":
        int_value_3 = tk.Label(frame, text="User Enable / Disable (0 == Disable / 1 == Enable)):", width=60)
        int_value_3.grid(row=5, column=0)
        int_value_3 = tk.Entry(frame)
        int_value_3.grid(row=5, column=1)
        int_value_3.insert(0, "0")
        entry_int_values.append(int_value_3)

        """
        Zero padding
        """
        int_value_4 = tk.Entry(frame)
        int_value_4.insert(0, "0")
        entry_int_values.append(int_value_4)

        int_value_5 = tk.Entry(frame)
        int_value_5.insert(0, "0")
        entry_int_values.append(int_value_5)

        int_value_6 = tk.Entry(frame)
        int_value_6.insert(0, "0")
        entry_int_values.append(int_value_6)

        int_value_7 = tk.Entry(frame)
        int_value_7.insert(0, "0")
        entry_int_values.append(int_value_7)

        """
        Send button
        """
        button_send = tk.Button(frame, text="Send", command=send_can_message)
        button_send.grid(row=20, columnspan=8, pady=10)

    elif selected_option == "Accel / Gyro Filtering (On / Off Toggle + Filter Parameters)":
        int_value_3 = tk.Label(frame, text="User Enable / Disable (0 == Disable / 1 == Enable)):", width=60)
        int_value_3.grid(row=5, column=0)
        int_value_3 = tk.Entry(frame)
        int_value_3.grid(row=5, column=1)
        int_value_3.insert(0, "0")
        entry_int_values.append(int_value_3)

        int_value_4 = tk.Label(frame, text="Accelerometer Filter Window Size (Number of samples (0-120)):", width=60)
        int_value_4.grid(row=6, column=0)
        int_value_4 = tk.Entry(frame)
        int_value_4.grid(row=6, column=1)
        int_value_4.insert(0, "0")
        entry_int_values.append(int_value_4)

        int_value_5 = tk.Label(frame, text="Gyroscope Filter Window Size (Number of samples (0-120)):", width=60)
        int_value_5.grid(row=7, column=0)
        int_value_5 = tk.Entry(frame)
        int_value_5.grid(row=7, column=1)
        int_value_5.insert(0, "0")
        entry_int_values.append(int_value_5)

        """
        Zero padding
        """
        int_value_6 = tk.Entry(frame)
        int_value_6.insert(0, "0")
        entry_int_values.append(int_value_6)

        int_value_7 = tk.Entry(frame)
        int_value_7.insert(0, "0")
        entry_int_values.append(int_value_7)

        """
        Send button
        """
        button_send = tk.Button(frame, text="Send", command=send_can_message)
        button_send.grid(row=20, columnspan=8, pady=10)

    elif selected_option == "Pro Mode":
        for _ in range(4):
            add_int_value_entry()


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

logo_image = Image.open("logo.png")
logo_image = logo_image.resize((400, 400), Image.ANTIALIAS)
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(frame, image=logo_photo)
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
    0x0:  "Please Select",
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

int_value2_var = tk.StringVar()
int_value2_var.trace("w", update_gui_options)  # Add this line here

label_int_value2 = tk.Label(frame, text="Control Parameter Selection:")
label_int_value2.grid(row=4, column=0)
entry_int_value2 = ttk.Combobox(frame, textvariable=int_value2_var, values=list(int_value2_options.values()), state='readonly')
entry_int_value2.grid(row=4, column=1)
entry_int_value2.set(list(int_value2_options.values())[0])  # Set the default value

root.mainloop()
