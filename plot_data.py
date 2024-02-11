import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

_COLORS = px.colors.qualitative.G10


_CASE_COLORS = {
    "BAU": "black",
    "ARC": _COLORS[1],
    "HUM": _COLORS[4],
    "PIR": _COLORS[0],
    "CRP": _COLORS[3],
}
LINE_CONF = {
    "BAU": {"color": _CASE_COLORS["BAU"], "dash": "solid", "width": 6},
    "ARC": {"color": _CASE_COLORS["ARC"], "dash": "longdash", "width": 6},
    "HUM": {"color": _CASE_COLORS["HUM"], "dash": "dashdot", "width": 6},
    "PIR": {"color": _CASE_COLORS["PIR"], "dash": "dot", "width": 6},
    "CRP": {"color": _CASE_COLORS["CRP"], "dash": "dash", "width": 6},
}
BOX_CONF = {
    "BAU": {"marker_color": _CASE_COLORS["BAU"]},
    "ARC": {"marker_color": _CASE_COLORS["ARC"]},
    "HUM": {"marker_color": _CASE_COLORS["HUM"]},
    "PIR": {"marker_color": _CASE_COLORS["PIR"]},
    "CRP": {"marker_color": _CASE_COLORS["CRP"]},
}

HEADER_RENAME = {"Consumption": "Energy", "Generated": "Costs"}
HEADER_FONT = 48
START_YEAR = 2010
START_YEAR = pd.Timestamp(2010, 1, 1)


def filter_date(df):
    if START_YEAR is not None:
        return df[df.Date >= START_YEAR].copy()


def plot_data_simple(df, cases, name, show=False, y_label="value", y_scale=None):
    # df = df[[n for n in df.columns if n.endswith("_mean") or n == "Year"]]
    fig = go.Figure()
    # df = df.rolling(ROLLING_MEAN_TICKS, on="Date").mean()
    df = filter_date(df)
    for case in cases:
        fig_ = go.Scatter(x=df.Date, y=df[f"{case}"], line=LINE_CONF[case], name=case)
        fig.add_trace(fig_)
    fig.update_layout(
        shapes=[go.layout.Shape(type="rect", xref="x domain", yref="y domain", x0=0, y0=0, x1=1, y1=1, line={"width": 2, "color": "black"})]
    )
    if y_scale:
        fig.update_layout(yaxis_range=y_scale)
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"size": HEADER_FONT},
        title={"text": name},
    )
    fig.update_yaxes(title_text=y_label, gridcolor="grey", showline=True, mirror=True)
    fig.update_xaxes(title_text="Year", gridcolor="grey", tickangle=320, showline=True, mirror=True)
    fig.write_image(f"plots/{name}.png", width=1680, height=1000, scale=1)
    if show:
        fig.show()


def plot_data_box(df, cases, name, show, y_label="value"):
    # get annual mean
    df = filter_date(df)
    df["Year"] = df.Date.dt.year
    df = df.drop("Date", axis=1).groupby("Year").mean().melt()
    fig = go.Figure()
    for case in cases:
        xdf = df[df.variable == case]
        fig.add_trace(go.Box(y=xdf.value, x=xdf.variable, **BOX_CONF[case], boxpoints="all", name=case))
    fig.update_layout(
        shapes=[go.layout.Shape(type="rect", xref="x domain", yref="y domain", x0=0, y0=0, x1=1, y1=1, line={"width": 2, "color": "black"})]
    )
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"size": HEADER_FONT},
        title={"text": name},
    )
    fig.update_yaxes(title_text=y_label, gridcolor="grey")
    fig.update_xaxes(title_text="Adaptation Measure", gridcolor="grey")
    fig.write_image(f"plots/{name}_box.png", width=1500, height=1200, scale=1)
    if show:
        fig.show()


def plot_data(df, name, cases, show=False, y_label="value", y_scale=None):
    if HEADER_RENAME.get(name.split(" ")[0]):
        name = " ".join([HEADER_RENAME.get(name.split(" ")[0])] + name.split(" ")[1:])
    name = HEADER_RENAME.get(name.split(" ")[0], name)
    plot_data_simple(df, cases, name, False, y_label, y_scale)
    plot_data_box(df, cases, name, False, y_label)


if __name__ == "__main__":
    df = pd.read_excel("test.xlsx")
    y_label = "mm/month"
    y_scale = (1, 2)
    plot_data(df, "test", show=True, y_label=y_label, y_scale=y_scale)
