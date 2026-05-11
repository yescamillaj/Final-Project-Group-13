import serial
import time
from collections import deque
 
# ── Serial / Arduino config
ARDUINO_PORT = "COM3"
BAUD_RATE = 9600
WARNING_DISTANCE = 50  # cm
 
ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
 
# ── Data storage
times = deque(maxlen=100)
distances = deque(maxlen=100)
start_time = time.time()
warning_count = 0
was_in_warning = False
 
print("Reading data from Arduino... Press Ctrl+C to stop.\n")
 

while True:
    try:
        raw = ser.readline().decode("utf-8").strip()
        if raw:
            distance = int(raw)
            current_time = time.time() - start_time
 
            times.append(current_time)
            distances.append(distance)
 
            if distance < WARNING_DISTANCE:
                status = "WARNING - Object Close!"
                if not was_in_warning:
                    warning_count += 1
                    was_in_warning = True
            else:
                status = "SAFE"
                was_in_warning = False
 
            print(f"Time: {current_time:.1f}s | Distance: {distance} cm | Status: {status} | Warnings: {warning_count}")
 
    except ValueError:
        pass
    except KeyboardInterrupt:
        print("\nStopped by user.")
        ser.close()
        break
    except Exception as e:
        print("Error:", e)
