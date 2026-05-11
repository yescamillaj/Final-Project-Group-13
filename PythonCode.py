import serial
import time
import tkinter as tk
from collections import deque
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


ARDUINO_PORT = "COM3"
BAUD_RATE = 9600

WARNING_DISTANCE = 50  # cm

ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

times = deque(maxlen=100)
distances = deque(maxlen=100)

start_time = time.time()
warning_count = 0
was_in_warning = False

root = tk.Tk()
root.title("Ultrasonic Blind Assist Glove Monitor")

distance_label = tk.Label(root, text="Distance: -- cm", font=("Arial", 20))
distance_label.pack()

status_label = tk.Label(root, text="Status: --", font=("Arial", 20))
status_label.pack()

warning_label = tk.Label(root, text="Warnings: 0", font=("Arial", 20))
warning_label.pack()

fig = Figure(figsize=(7, 4))
ax = fig.add_subplot(111)
ax.set_title("Distance vs Time")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Distance (cm)")
ax.set_ylim(0, 100)

line, = ax.plot([], [], label="Distance")
ax.axhline(WARNING_DISTANCE, linestyle="--", label="Warning limit: 50 cm")
ax.legend()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

def update_data():
    global warning_count, was_in_warning

    try:
        raw_data = ser.readline().decode("utf-8").strip()

        if raw_data:
            distance = int(raw_data)

            current_time = time.time() - start_time

            times.append(current_time)
            distances.append(distance)

            distance_label.config(text=f"Distance: {distance} cm")

            if distance < WARNING_DISTANCE:
                status_label.config(text="Status: WARNING - Object close")

                # Counts one warning per approach
                if not was_in_warning:
                    warning_count += 1
                    was_in_warning = True
            else:
                status_label.config(text="Status: SAFE")
                was_in_warning = False

            warning_label.config(text=f"Warnings: {warning_count}")

            line.set_data(times, distances)

            if len(times) > 1:
                ax.set_xlim(max(0, times[0]), times[-1] + 1)

            canvas.draw()

    except ValueError:
        pass
    except Exception as e:
        print("Error:", e)

    root.after(200, update_data)

def close_program():
    ser.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_program)

update_data()
root.mainloop()