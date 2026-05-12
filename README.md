## Code Structure

The code is divided into 4 branches:

| Branch | Description |
|---|---|
| `main` | Full working code (Arduino + Dashboard + ThingSpeak) |
| `dashboard` | Only the GUI dashboard |
| `data-reading` | Only the Arduino serial data reader |
| `thingSpeak` | Only the ThingSpeak data logging |

---

## Branch 1: Main
Contains the complete code combining all three modules:
- Reads distance data from the Arduino via serial port
- Displays a live GUI dashboard using Dash/Plotly
- Sends data to ThingSpeak every 15 seconds

**Key settings:**
- Port: `COM3` | Baud rate: `9600`
- Warning threshold: `50 cm`
- ThingSpeak update interval: `15 seconds`

---

## Branch 2: Dashboard
Contains only the Dash/Plotly GUI dashboard.
- Live distance display (in cm)
- Status indicator: `SAFE` (green) or `WARNING` (red)
- Total warning counter
- Real-time distance vs. time graph with a warning limit line at 50 cm
- Refreshes every 500 ms

> Note: In this branch, no real Arduino data is read. The main, has the full code which reads the data from Arduino
---

## Branch 3: Data-Reading
Contains only the Arduino serial reader.

**What it does:**
- Connects to the Arduino on `COM3` at `9600` baud
- Reads distance values continuously
- Detects when an object is closer than `50 cm` and counts warnings
- Prints live readings to the console:
  `Time | Distance | Status | Warning Count`

---

## Branch 4: ThingSpeak
Contains the Arduino reader **plus** ThingSpeak integration.

**What it does:**
- Same serial reading as the `data-reading` branch
- Every 15 seconds, sends data to ThingSpeak:
  - `Field 1`: Distance (cm)
  - `Field 2`: Total warning count
