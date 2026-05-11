import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
 
# ── Simulated data (replace with real data in main branch) ──────────
# In the full version, this data comes from the Arduino serial reader
times = []
distances = []
warning_count = 0
latest_distance = None
latest_status = "No data — connect Arduino to read live data"
WARNING_DISTANCE = 50  # cm
 
#  Dash app layout
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
            "🧤 Blind Assist Glove Monitor",
            style={"textAlign": "center", "color": "#38bdf8", "marginBottom": "30px"},
        ),
 
        #Stat cards
        html.Div(
            style={"display": "flex", "justifyContent": "center", "gap": "20px", "flexWrap": "wrap"},
            children=[
                # Distance card
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
                        html.P("Distance", style={"color": "#94a3b8", "margin": 0, "fontSize": "14px"}),
                        html.H2(id="distance-text", style={"margin": "8px 0", "fontSize": "2.5rem", "color": "#38bdf8"}),
                    ],
                ),
                # Status card
                html.Div(
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
                # Warning count card
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
 
        #Live chart
        html.Div(
            style={"marginTop": "30px"},
            children=[dcc.Graph(id="live-graph", style={"height": "400px"})],
        ),
 
        #Auto-refresh every 500 ms
        dcc.Interval(id="interval", interval=500, n_intervals=0),
    ],
)
 
#  Callbacks
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
 
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(times), y=list(distances),
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
    print("\n🌐  Dashboard running at:  http://127.0.0.1:8050\n")
    app.run(debug=False)
