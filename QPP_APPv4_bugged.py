"""
TSLA intraday chart
Daily  : anchor = current_day_idr_midpoint,  round ±5/10/15 USD
Weekly : anchor = Tuesday‑IDR midpoint,      round ±10/20/30 USD
Each session gets its *own* logistic curve (3 anchors → logit fit) so
probabilities vary day‑by‑day / week‑by‑week.
"""
import datetime
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
from zoneinfo import ZoneInfo
from typing import Any, cast

# ───────────────────────────  CONSTANTS & PATHS
st.set_page_config(page_title="TSLA round levels", layout="wide")
NY   = ZoneInfo("America/New_York")
ROOT = "https://raw.githubusercontent.com/loop16/models/main/"
PRICE_PATH  = ROOT + "BATS_TSLAext%2C%205.csv"
LEVEL_PATH  = ROOT + "tesla_actual_levels_minimal.csv"
WLEVEL_PATH = ROOT + "tesla_weekly_actual_levels_minimal.csv"

# ───────────────────────────  PILL BUTTONS
def pill_buttons(options, *, key, index=0, colors=None,
                 container=st, horizontal=True):
    if key not in st.session_state:
        st.session_state[key] = options[index]
    cols = container.columns(len(options)) if horizontal else [container]
    for opt, col in zip(options, cols):
        active = st.session_state[key] == opt
        bg = colors.get(opt, "#E4E4E4") if active and colors else \
             "#E4E4E4" if active else "#F5F5F5"
        fg = "white" if active and colors and opt in colors else "black"
        k  = f"{key}_{opt}"
        with col:
            if st.button(opt.upper(), key=k, use_container_width=True):
                st.session_state[key] = opt
        st.markdown(f"""
        <style>
        div[data-key="{k}"] *:last-child button {{
            background:{bg}!important;color:{fg}!important;border:none!important;
            border-radius:0.65rem!important;padding:0.35rem 0.9rem!important;
            font-weight:600!important;cursor:pointer!important;
        }}</style>""", unsafe_allow_html=True)
    return st.session_state[key]

# ───────────────────────────  LOAD DATA
@st.cache_data
def load_5m(url:str)->pd.DataFrame:
    df = pd.read_csv(url)
    df["time"]    = pd.to_datetime(df["time"], utc=True)
    df["epoch"]   = (df["time"].astype("int64") // 10**9).astype(int)
    df["ny_date"] = df["time"].dt.tz_convert(NY).dt.date
    df["ny_time"] = df["time"].dt.tz_convert(NY).dt.time
    return df[["epoch","open","high","low","close","ny_date","ny_time"]]

@st.cache_data
def resample(df:pd.DataFrame, rule:str)->pd.DataFrame:
    out = (df.set_index(pd.to_datetime(df["epoch"],unit="s",utc=True))
             .resample(rule,label="right",closed="right")
             .agg({"open":"first","high":"max","low":"min","close":"last"})
             .dropna())
    out["epoch"]   = (out.index.astype("int64") // 10**9).astype(int)
    out["ny_date"] = out.index.tz_convert(NY).date
    out["ny_time"] = out.index.tz_convert(NY).time
    return out.reset_index(drop=True)

raw_5m = load_5m(PRICE_PATH)
raw_15, raw_30, raw_1h = [resample(raw_5m, r) for r in ("15T", "30T", "1H")]

@st.cache_data
def load_daily(url:str)->pd.DataFrame:
    d = pd.read_csv(url)
    d["date"] = pd.to_datetime(d["analysis_date"]).dt.date
    return d
daily_df = load_daily(LEVEL_PATH)

@st.cache_data
def load_weekly(url:str)->pd.DataFrame:
    w = pd.read_csv(url)
    w["tuesday_idr_midpoint"] = pd.to_numeric(w["tuesday_idr_midpoint"],
                                              errors="coerce")
    tue = pd.to_datetime(w["analysis_start_tuesday"]).dt.date
    w["tuesday"] = tue
    wed  = (pd.to_datetime(tue + pd.Timedelta(days=1)) +
            pd.Timedelta(hours=5))        # Wed 05 :00 NY
    tueN = (pd.to_datetime(tue + pd.Timedelta(days=7)) +
            pd.Timedelta(hours=5))        # Tue 05 :00 NY
    w["start_epoch"] = (wed.dt.tz_localize(NY).dt.tz_convert("UTC")
                        .view("int64") // 10**9).astype(int)
    w["end_epoch"]   = (tueN.dt.tz_localize(NY).dt.tz_convert("UTC")
                        .view("int64") // 10**9).astype(int)
    return w
weekly_df = load_weekly(WLEVEL_PATH)

# attach 08:30 open (useful later if needed)
opens830 = raw_5m[raw_5m["ny_time"] == datetime.time(8,30)]\
             [["ny_date","open"]].rename(columns={"open":"open_830"})
daily_df  = daily_df.merge(opens830, left_on="date", right_on="ny_date",  how="left")
weekly_df = weekly_df.merge(opens830,
                left_on=weekly_df["tuesday"] + pd.Timedelta(days=1),
                right_on="ny_date", how="left")

# ───────────────────────────  PER‑ROW LOGISTIC FIT
def _ab_from_row(row, side:str, kind:str):
    """
    Return (a,b) for this row/side using its own 80/50/20 anchors.
    long  : high‑80 = 80 %, high‑50 = 50 %, high‑20 = 20 %
    short : low‑20  = 20 %, low‑50  = 50 %, low‑80 = 80 %
    """
    mid = row["current_day_idr_midpoint"] if kind=="daily" else row["tuesday_idr_midpoint"]
    if pd.isna(mid):
        return None

    if side == "long":
        anchors = [("high_20_level", 0.80),   # ← 20‑level ⇒ 80 %
                   ("high_50_level", 0.50),
                   ("high_80_level", 0.20)] 
    else:
        anchors = [("low_20_level", 0.20),
                   ("low_50_level", 0.50),
                   ("low_80_level", 0.80)]

    dists, probs = [], []
    for col, p in anchors:
        v = row.get(col)
        if pd.notna(v):
            dists.append(abs(v - mid))
            probs.append(p)

    if len(dists) < 3:          # need all three points – otherwise skip
        return None

    logit = np.log(np.array(probs) / (1 - np.array(probs)))
    b, a = np.polyfit(dists, logit, 1)     # slope, intercept
    return a, b


def _prob_from_ab(ab, Δ: float) -> float:
    """Clamp to 1 – 99 % before labelling."""
    a, b = ab
    p = 1 / (1 + np.exp(-(a + b * Δ)))
    return min(max(p, 0.01), 0.99)         # 1 – 99 %

# ───────────────────────────  SIDEBAR
with st.sidebar:
    tf   = pill_buttons(["5 m","15 m","30 m","1 h"], key="tf",  index=1)
    view = pill_buttons(["Daily","Weekly"],          key="vw",  index=0)
    mode = pill_buttons(["long","short","both"],     key="side",index=0,
                        colors={"long":"#26A69A","short":"#EF5350"})

    if view == "Daily":
        N_days  = st.slider("Trading days", 1, 20, 6)
        N_weeks = 6
    else:
        N_weeks = st.slider("Weekly windows", 1, 20, 6)
        N_days  = 6

frame = {"5 m": raw_5m, "15 m": raw_15, "30 m": raw_30, "1 h": raw_1h}[tf]

if view == "Daily":
    keep_dates = sorted(raw_5m["ny_date"].unique())[-N_days:]
    df_view = frame[frame["ny_date"].isin(keep_dates)].copy()
else:
    keep_weeks = weekly_df.sort_values("tuesday")["tuesday"].unique()[-N_weeks:]
    start_ep   = int(weekly_df[weekly_df["tuesday"].isin(keep_weeks)]["start_epoch"].min())
    df_view    = frame[frame["epoch"] >= start_ep].copy()

# ───────────────────────────  BUILD LEVEL LINES
def _make_line(t0, t1, price, label, color, style):
    return {"type":"Line",
            "data":[{"time":t0,"value":price},{"time":t1,"value":price}],
            "markers":[{"time":t1,"position":"inBar","shape":"text",
                        "text":label,"color":color,"size":1}],
            "options":{"priceScaleId":"right","priceLineVisible":False,
                       "lastValueVisible":False,"color":color,
                       "lineWidth":2,"lineStyle":style}}

level_series = []

# ---- DAILY ----
if view == "Daily":
    intraday = (df_view["ny_time"] >= datetime.time(9,30)) & \
               (df_view["ny_time"] <= datetime.time(15,55))

    for d, grp in df_view[intraday].groupby("ny_date"):
        row = daily_df.loc[daily_df["date"] == d].squeeze()
        mid = row.get("current_day_idr_midpoint")
        if pd.isna(mid):
            continue
        mid_round = round(mid / 5) * 5
        t0, t1 = int(grp["epoch"].iat[0]), int(grp["epoch"].iat[-1])

        for side, steps in [("long", [5,10,15]),
                            ("short",[-5,-10,-15])]:
            if mode != "both" and side != mode:
                continue
            ab   = _ab_from_row(row, side, "daily")
            col  = "#26A69A" if side=="long" else "#EF5350"
            styl = 0 if side=="long" else 2

            for st in steps:
                target = mid_round + st
                p = _prob_from_ab(ab, abs(target - mid)) if ab else 0.5
                label = f"{target:.0f}  {p*100:.0f}%"
                level_series.append(_make_line(t0, t1, target, label, col, styl))

# ---- WEEKLY ----
else:
    keep_weeks = weekly_df.sort_values("tuesday")["tuesday"].unique()[-N_weeks:]
    for wk in weekly_df[weekly_df["tuesday"].isin(keep_weeks)].itertuples():
        row = pd.Series(wk._asdict())
        mid = row["tuesday_idr_midpoint"]
        if pd.isna(mid):
            continue
        mid_round = round(mid / 10) * 10
        t0, t1 = int(row["start_epoch"]), int(row["end_epoch"])

        for side, steps in [("long", [10,20,30]),
                            ("short",[-10,-20,-30])]:
            if mode != "both" and side != mode:
                continue
            ab   = _ab_from_row(row, side, "weekly")
            col  = "#26A69A" if side=="long" else "#EF5350"
            styl = 0 if side=="long" else 2

            for st in steps:
                target = mid_round + st
                p = _prob_from_ab(ab, abs(target - mid)) if ab else 0.5
                label = f"{target:.0f}  {p*100:.0f}%"
                level_series.append(_make_line(t0, t1, target, label, col, styl))

# ───────────────────────────  CANDLES & CHART
bars=[{"time":int(r.epoch),"open":float(r.open),"high":float(r.high),
       "low":float(r.low),"close":float(r.close)} for r in df_view.itertuples(index=False)]
start=max(len(bars)-120, 0); end=len(bars)-1
candles={"type":"Candlestick","data":bars,
         "options":{"priceScaleId":"right","priceLineVisible":False,
                    "upColor":"#26A69A","downColor":"#EF5350",
                    "wickUpColor":"#26A69A","wickDownColor":"#EF5350",
                    "borderUpColor":"#26A69A","borderDownColor":"#EF5350"}}

chart_cfg=[{
    "chart":{"height":900,
             "layout":{"background":{"color":"#0E1117"},"textColor":"#D1D4DC"},
             "grid":{"vertLines":{"color":"#2B3139"},"horzLines":{"color":"#2B3139"}},
             "timeScale":{"rightOffset":0,
                          "visibleLogicalRange":{"from":start,"to":end}},
             "crosshair":{"mode":0,
                          "vertLine":{"labelVisible":False},
                          "horzLine":{"labelVisible":True,
                                      "labelBackgroundColor":"#444C55",
                                      "labelTextColor":"#FFFFFF"}},
             "rightPriceScale":{"visible":True,"borderVisible":True,
                                "borderColor":"#444C55"}},
    "series":[candles,*level_series]
}]
renderLightweightCharts(cast(Any,chart_cfg), key="tsla_chart")
