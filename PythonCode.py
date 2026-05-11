import serial
import time
import threading
from collections import deque
 
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
 
ARDUINO_PORT = "COM3"
BAUD_RATE = 9600
WARNING_DISTANCE = 50  
ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
 
times = deque(maxlen=100)
distances = deque(maxlen=100)
start_time = time.time()
warning_count = 0
was_in_warning = False
latest_distance = None
latest_status = "Initializing…"
 
def read_serial():
    global warning_count, was_in_warning, latest_distance, latest_status
    while True:
        try:
            raw = ser.readline().decode("utf-8").strip()
            if raw:
                distance = int(raw)
                t = time.time() - start_time
                times.append(t)
                distances.append(distance)
                latest_distance = distance
 
                if distance < WARNING_DISTANCE:
                    latest_status = "WARNING — Object Close!"
                    if not was_in_warning:
                        warning_count += 1
                        was_in_warning = True
                else:
                    latest_status = "SAFE"
                    was_in_warning = False
        except ValueError:
            pass
        except Exception as e:
            print("Serial error:", e)
 
threading.Thread(target=read_serial, daemon=True).start()

 
#Dash app layout
app = dash.Dash(__name__)
app.title = "Blind Assist Glove Monitor"
 
app.layout = html.Div(
    style={
        "fontFamily": "'Segoe UI', sans-serif",
        "backgroundColor": "#0f172a",
        "minHeight": "100vh",
        "padding": "30px",
        "color": "#f1f5f9",
    },
    children=[
        html.H1(
            "Blind Assist Glove Monitor",
            style={"textAlign": "center", "color": "#38bdf8", "marginBottom": "30px"},
        ),
 
        html.Div(
            style={"display": "flex", "justifyContent": "center", "gap": "20px", "flexWrap": "wrap"},
            children=[
                html.Div(
                    id="distance-card",
                    style={
                        "backgroundColor": "#1e293b",
                        "borderRadius": "12px",
                        "padding": "24px 40px",
                        "textAlign": "center",
                        "minWidth": "200px",
                        "boxShadow": "0 4px 20px rgba(0,0,0,0.4)",
                    },
                    children=[
                        html.P("Distance", style={"color": "#94a3b8", "margin": 0, "fontSize": "14px"}),
                        html.H2(id="distance-text", style={"margin": "8px 0", "fontSize": "2.5rem", "color": "#38bdf8"}),
                    ],
                ),
                html.Div(
                    id="status-card",
                    style={
                        "backgroundColor": "#1e293b",
                        "borderRadius": "12px",
                        "padding": "24px 40px",
                        "textAlign": "center",
                        "minWidth": "250px",
                        "boxShadow": "0 4px 20px rgba(0,0,0,0.4)",
                    },
                    children=[
                        html.P("Status", style={"color": "#94a3b8", "margin": 0, "fontSize": "14px"}),
                        html.H2(id="status-text", style={"margin": "8px 0", "fontSize": "1.6rem"}),
                    ],
                ),

                html.Div(
                    style={
                        "backgroundColor": "#1e293b",
                        "borderRadius": "12px",
                        "padding": "24px 40px",
                        "textAlign": "center",
                        "minWidth": "200px",
                        "boxShadow": "0 4px 20px rgba(0,0,0,0.4)",
                    },
                    children=[
                        html.P("Total Warnings", style={"color": "#94a3b8", "margin": 0, "fontSize": "14px"}),
                        html.H2(id="warning-text", style={"margin": "8px 0", "fontSize": "2.5rem", "color": "#f97316"}),
                    ],
                ),
            ],
        ),
 

        html.Div(
            style={"marginTop": "30px"},
            children=[
                dcc.Graph(id="live-graph", style={"height": "400px"}),
            ],
        ),
 

        dcc.Interval(id="interval", interval=500, n_intervals=0),
    ],
)
 
# Callbacks
@app.callback(
    Output("distance-text", "children"),
    Output("status-text", "children"),
    Output("status-text", "style"),
    Output("warning-text", "children"),
    Output("live-graph", "figure"),
    Input("interval", "n_intervals"),
)
def update_dashboard(_):

    dist_text = f"{latest_distance} cm" if latest_distance is not None else "-- cm"
 


    if latest_distance is not None and latest_distance < WARNING_DISTANCE:
        status_style = {"margin": "8px 0", "fontSize": "1.6rem", "color": "#ef4444"}
    else:
        status_style = {"margin": "8px 0", "fontSize": "1.6rem", "color": "#22c55e"}
 

    t_list = list(times)
    d_list = list(distances)
 
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t_list, y=d_list,
        mode="lines+markers",
        name="Distance",
        line=dict(color="#38bdf8", width=2),
        marker=dict(size=4),
    ))
    fig.add_hline(
        y=WARNING_DISTANCE,
        line_dash="dash",
        line_color="#ef4444",
        annotation_text="Warning limit: 50 cm",
        annotation_position="bottom right",
    )
    fig.update_layout(
        paper_bgcolor="#1e293b",
        plot_bgcolor="#0f172a",
        font=dict(color="#f1f5f9"),
        title=dict(text="Distance vs Time", font=dict(size=18, color="#38bdf8")),
        xaxis=dict(title="Time (s)", gridcolor="#334155"),
        yaxis=dict(title="Distance (cm)", range=[0, 100], gridcolor="#334155"),
        margin=dict(l=50, r=30, t=50, b=50),
        legend=dict(bgcolor="#1e293b"),
    )
 
    return dist_text, latest_status, status_style, str(warning_count), fig
 
 
#Run
if __name__ == "__main__":
    print("\nDashboard running at:  http://127.0.0.1:8050\n")
    app.run(debug=False)
