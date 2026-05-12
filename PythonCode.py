import serial
import time
from collections import deque
import requests
 
#Arduino config
ARDUINO_PORT = "COM3"
BAUD_RATE = 9600
WARNING_DISTANCE = 50  # cm
 
#ThingSpeak config
THINGS_API_KEY = "OFO25QKX8G98J3QN"
THINGSPEAK_URL = "https://api.thingspeak.com/update"
last_send_time = 0
 
ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
time.sleep(2)


times = deque(maxlen=100)
distances = deque(maxlen=100)
start_time = time.time()
warning_count = 0
was_in_warning = False
 
 
def enviar_thingspeak(distance, warning_count):
    payload = {
        "api_key": THINGS_API_KEY,
        "field1": distance,
        "field2": warning_count
    }
    try:
        response = requests.post(THINGSPEAK_URL, data=payload, timeout=3)
        if response.status_code == 200:
            print(f"Dato enviado: Distancia {distance}, Alertas {warning_count}")
        else:
            print(f"Error de ThingSpeak: Código {response.status_code}")
    except Exception as e:
        print("Error de conexión:", e)
 
 
print("Reading data from Arduino and sending to ThingSpeak... Press Ctrl+C to stop.\n")
 
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
 
            # Send to ThingSpeak every 15 seconds
            if current_time - last_send_time > 15:
                enviar_thingspeak(distance, warning_count)
                last_send_time = current_time
 
    except ValueError:
        pass
    except KeyboardInterrupt:
        print("\nStopped by user.")
        ser.close()
        break
    except Exception as e:
        print("Error:", e)
