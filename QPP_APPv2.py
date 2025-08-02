"""
TSLA intraday chart – Daily / Weekly 20- 50- 80 % levels
────────────────────────────────────────────────────────────────────────
Daily  : intraday lines from 09:30 → 15:55 NY, taken straight from the
         H20 / H50 / H80 (long) and L20 / L50 / L80 (short) columns.
         AUTO = choose long/short per day:
                if 09:30 open > 10:25 close  ⇒ short levels
                else                         ⇒ long  levels
Weekly : Wednesday 05:00 NY → Tuesday 05:00 NY window, using the weekly
         CSV.  AUTO behaves like BOTH (shows both long + short sets).
"""
import datetime, uuid
from typing import Any, cast

import pandas as pd
import streamlit as st
from zoneinfo import ZoneInfo
from streamlit_lightweight_charts import renderLightweightCharts

# ───────────────────────────  GLOBAL & PATHS
st.set_page_config(page_title="TSLA levels", layout="wide")
NY   = ZoneInfo("America/New_York")
ROOT = "https://raw.githubusercontent.com/loop16/models/main/"
PRICE_PATH  = ROOT + "BATS_TSLAext%2C%205.csv"
LEVEL_PATH  = ROOT + "tesla_actual_levels_minimal.csv"
WLEVEL_PATH = ROOT + "tesla_weekly_actual_levels_minimal.csv"

# ───────────────────────────  PILL BUTTON UI
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

# ───────────────────────────  LOAD & RESAMPLE PRICE DATA
@st.cache_data
def load_5m(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    df["time"]  = pd.to_datetime(df["time"], utc=True)
    df["epoch"] = (df["time"].astype("int64") // 10**9).astype(int)
    df["ny_date"] = df["time"].dt.tz_convert(NY).dt.date
    df["ny_time"] = df["time"].dt.tz_convert(NY).dt.time
    return df[["epoch","open","high","low","close","ny_date","ny_time"]]

@st.cache_data
def resample(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    out = (df.set_index(pd.to_datetime(df["epoch"], unit="s", utc=True))
             .resample(rule, label="right", closed="right")
             .agg({"open":"first","high":"max","low":"min","close":"last"})
             .dropna())
    out["epoch"]   = (out.index.astype("int64") // 10**9).astype(int)
    out["ny_date"] = out.index.tz_convert(NY).date
    out["ny_time"] = out.index.tz_convert(NY).time
    return out.reset_index(drop=True)

raw_5m = load_5m(PRICE_PATH)
raw_15, raw_30, raw_1h = [resample(raw_5m, r) for r in ("15T","30T","1H")]

# 09:30 open & 10:25 close maps  (for AUTO)
open0930  = raw_5m[raw_5m["ny_time"]==datetime.time(9,30)]\
              .set_index("ny_date")["open"].to_dict()
close1025 = raw_5m[raw_5m["ny_time"]==datetime.time(10,25)]\
              .set_index("ny_date")["close"].to_dict()

# ───────────────────────────  LEVEL CSVs
@st.cache_data
def load_daily(url:str)->pd.DataFrame:
    d = pd.read_csv(url)
    d["date"] = pd.to_datetime(d["analysis_date"]).dt.date
    return d
daily_df = load_daily(LEVEL_PATH)

@st.cache_data
def load_weekly(url:str)->pd.DataFrame:
    w = pd.read_csv(url)
    tue = pd.to_datetime(w["analysis_start_tuesday"]).dt.date
    w["tuesday"] = tue
    wed  = (pd.to_datetime(tue + pd.Timedelta(days=1)) + pd.Timedelta(hours=5))
    tueN = (pd.to_datetime(tue + pd.Timedelta(days=7)) + pd.Timedelta(hours=5))
    w["start_epoch"] = (wed.dt.tz_localize(NY).dt.tz_convert("UTC")
                        .view("int64")//10**9).astype(int)
    w["end_epoch"]   = (tueN.dt.tz_localize(NY).dt.tz_convert("UTC")
                        .view("int64")//10**9).astype(int)
    return w
weekly_df = load_weekly(WLEVEL_PATH)

# ───────────────────────────  CONSTANT MAPS
cols_map = {
    "long":  ["high_20_level", "high_50_level", "high_80_level"],
    "short": ["low_20_level",  "low_50_level",  "low_80_level"],
}
label_map = {
    "high_20_level":"80% to reach","high_50_level":"50% to reach","high_80_level":"20% to reach",
    "low_20_level" :"20% to reach","low_50_level" :"50% to reach","low_80_level" :"80% to reach",
}

def style_for(side:str):
    return {"color":"#26A69A" if side=="long" else "#EF5350",
            "lineStyle":0 if side=="long" else 2}

def make_line(t0:int,t1:int,price:float,label:str,side:str):
    sty = style_for(side)
    return {"type":"Line",
            "data":[{"time":t0,"value":price},{"time":t1,"value":price}],
            "markers":[{"time":t1,"position":"inBar","shape":"text",
                        "text":label,"color":sty["color"],"size":1}],
            "options":{"priceScaleId":"right","priceLineVisible":False,
                       "lastValueVisible":False,"color":sty["color"],
                       "lineWidth":2,"lineStyle":sty["lineStyle"]}}

# ───────────────────────────  SIDEBAR
with st.sidebar:
    tf   = pill_buttons(["5 m","15 m","30 m","1 h"],key="tf",index=1)
    view = pill_buttons(["Daily","Weekly"],         key="vw",index=0)
    side_sel = pill_buttons(["long","short","both","auto"], key="side",index=0,
                            colors={"long":"#26A69A","short":"#EF5350"})
    if view=="Daily":
        N_days  = st.slider("Trading days",1,20,6); N_weeks=6
    else:
        N_weeks = st.slider("Weekly windows",1,20,6); N_days=6

frame = {"5 m":raw_5m,"15 m":raw_15,"30 m":raw_30,"1 h":raw_1h}[tf]

if view=="Daily":
    keep_dates = sorted(raw_5m["ny_date"].unique())[-N_days:]
    df_view    = frame[frame["ny_date"].isin(keep_dates)].copy()
else:
    keep_weeks = weekly_df.sort_values("tuesday")["tuesday"].unique()[-N_weeks:]
    first_ep   = int(weekly_df[weekly_df["tuesday"].isin(keep_weeks)]["start_epoch"].min())
    df_view    = frame[frame["epoch"]>=first_ep].copy()

# ───────────────────────────  BUILD LEVEL LINES
level_series=[]

# DAILY ---------------------------------------------------------------
def add_daily_lines(day_df:pd.DataFrame):
    date = day_df["ny_date"].iat[0]
    t0,t1 = int(day_df["epoch"].iat[0]), int(day_df["epoch"].iat[-1])
    row = daily_df.loc[daily_df["date"]==date].squeeze()
    if row.empty: return

    # decide which sides to draw
    if side_sel=="both":
        active=["long","short"]
    elif side_sel in ("long","short"):
        active=[side_sel]
    else:   # auto
        op=open0930.get(date); cls=close1025.get(date)
        active=["short"] if (op is not None and cls is not None and op>cls) else ["long"]

    for side in active:
        for col in cols_map[side]:
            val=row.get(col)
            if pd.notna(val):
                level_series.append(make_line(t0,t1,float(val),label_map[col],side))

# WEEKLY --------------------------------------------------------------
def add_weekly_lines(row:pd.Series):
    t0,t1 = int(row["start_epoch"]), int(row["end_epoch"])
    if side_sel=="long":   sides=["long"]
    elif side_sel=="short":sides=["short"]
    else:                  sides=["long","short"]   # both / auto

    for side in sides:
        for col in cols_map[side]:
            val=row.get(col)
            if pd.notna(val):
                level_series.append(make_line(t0,t1,float(val),label_map[col],side))

# build
if view=="Daily":
    intramask=(df_view["ny_time"]>=datetime.time(9,30)) & \
              (df_view["ny_time"]<=datetime.time(15,55))
    for _,g in df_view[intramask].groupby("ny_date"):
        add_daily_lines(g)
else:
    for wk in weekly_df[weekly_df["tuesday"].isin(keep_weeks)].itertuples():
        add_weekly_lines(pd.Series(wk._asdict()))

# ───────────────────────────  CANDLES & CHART
bars=[{"time":int(r.epoch),"open":float(r.open),"high":float(r.high),
       "low":float(r.low),"close":float(r.close)} for r in df_view.itertuples(index=False)]
start=max(len(bars)-120,0); end=len(bars)-1
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
