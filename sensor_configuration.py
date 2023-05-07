import tkinter as tk
from tkinter import messagebox
import can
import cantools

def send_can_message():
	try:
		channel = entry_channel.get()
		bitrate = int(entry_bitrate.get())

		bus = can.interface.Bus(channel=channel, bustype='pcan', bitrate=bitrate)

		float_value = float(entry_float_value.get())
		int_value = int(float_value / 0.01) # Convert the float to an integer scaled by 0.01

		arbitration_id = int(entry_can_id.get(), 16)
		data = int_value.to_bytes(6, byteorder='big')  # Convert the integer to a two-byte value

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

label_channel = tk.Label(frame, text="Channel:")
label_channel.grid(row=0, column=0)
entry_channel = tk.Entry(frame)
entry_channel.grid(row=0, column=1)
entry_channel.insert(0, "PCAN_USBBUS1")

label_bitrate = tk.Label(frame, text="Bitrate (bps):")
label_bitrate.grid(row=1, column=0)
entry_bitrate = tk.Entry(frame)
entry_bitrate.grid(row=1, column=1)
entry_bitrate.insert(0, "1000000")

label_can_id = tk.Label(frame, text="CAN ID:")
label_can_id.grid(row=2, column=0)
entry_can_id = tk.Entry(frame)
entry_can_id.grid(row=2, column=1)
entry_can_id.insert(0, "6")

label_float_value = tk.Label(frame, text="Float Value:")
label_float_value.grid(row=3, column=0)
entry_float_value = tk.Entry(frame)
entry_float_value.grid(row=3, column=1)

button_send = tk.Button(frame, text="Send", command=send_can_message)
button_send.grid(row=4, columnspan=2, pady=10)

root.mainloop()