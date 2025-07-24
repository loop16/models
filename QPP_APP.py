"""
TSLA intraday chart – Daily/Weekly levels, with labelled tags (H20, … / L20, …)
attached to the right‑hand end of each horizontal level line.
"""

import datetime
from typing import Any, cast

import pandas as pd
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
from zoneinfo import ZoneInfo

import streamlit as st, uuid


st.set_page_config(page_title="TSLA levels", layout="wide")


def pill_buttons(
    options,                     # list[str]
    *,                           # — keyword‑only —
    key: str,
    index: int = 0,
    colors: dict[str, str] | None = None,   # {opt:bg_hex}
    horizontal: bool = True,
    container = st,              # where to put the pills
):
    """Return the selected option from a group of coloured pill buttons."""
    if key not in st.session_state:
        st.session_state[key] = options[index]

    gap = "small"
    cols = (
        container.columns(len(options), gap=gap)
        if horizontal
        else [container.container() for _ in options]
    )

    for opt, col in zip(options, cols):
        active = st.session_state[key] == opt
        bg = (
            colors.get(opt, "#E4E4E4") if (active and colors)             # coloured active
            else "#E4E4E4" if active                                      # grey active
            else "#F5F5F5"                                                # grey inactive
        )
        fg = "white" if (active and colors and opt in colors) else "black"
        btn_key = f"{key}_{opt}"

        with col:
            clicked = st.button(
                opt.upper(),
                key=btn_key,
                use_container_width=True,
            )

        # high‑specificity CSS with !important to beat Streamlit’s theme
        st.markdown(
            f"""
            <style>
            /* select the *button element* = last child under the stButton wrapper */
            div[data-testid="stButton"][data-key="{btn_key}"] *:last-child button {{
                background:{bg} !important;
                color:{fg} !important;
                border:none !important;
                border-radius:0.65rem !important;
                padding:0.35rem 0.9rem !important;
                font-weight:600 !important;
                cursor:pointer !important;
                transition:filter .15s !important;
            }}
            div[data-testid="stButton"][data-key="{btn_key}"] *:last-child button:hover {{
                filter:brightness(1.10) !important;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )


        if clicked:
            st.session_state[key] = opt

    return st.session_state[key]




# ── file paths ───────────────────────────────────────────────────────
PRICE_PATH  = "https://raw.githubusercontent.com/loop16/models/refs/heads/main/BATS_TSLAext%2C%205.csv"
LEVEL_PATH  = "https://raw.githubusercontent.com/loop16/models/main/tesla_actual_levels_minimal.csv"
WLEVEL_PATH = "https://raw.githubusercontent.com/loop16/models/main/tesla_weekly_actual_levels_minimal.csv"


NY = ZoneInfo("America/New_York")

# ────────────────────────────────────────────────────────────────
# 0.  Tiny helper to draw a button‑group selector
# ────────────────────────────────────────────────────────────────
import uuid
from typing import List

def button_group(
    options: List[str],
    *,
    index: int = 0,
    format_func=lambda x: x,
    key: str | None = None,
    color_map: dict[str, str] | None = None,
    horizontal: bool = True,
) -> str:
    
    import streamlit as _st

    if key is None:
        key = f"_btn_grp_{uuid.uuid4().hex}"

    # one‑time CSS (scoped by key → avoids clashing with other groups)
    if f"{key}_css" not in _st.session_state:
        gap = "small"
        st.markdown(
            f"""
            <style>
            /* target the <button> inside the sidebar hierarchy ★ */
            div[data-key="{btn_key}"] button[data-baseweb="button"] {{
                background:{bg} !important;      /* selected / neutral */
                color:{fg} !important;
                border:none !important;
                border-radius:0.65rem !important;
                padding:0.35rem 0.9rem !important;
                font-weight:600 !important;
                cursor:pointer !important;
                transition:filter .15s !important;
            }}
            div[data-key="{btn_key}"] button[data-baseweb="button"]:hover {{
                filter:brightness(1.10) !important;          /* hover brighten */
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

        _st.session_state[f"{key}_css"] = True

    # first run → set default
    if key not in _st.session_state:
        _st.session_state[key] = options[index]

    # layout
    cols = _st.columns(len(options)) if horizontal else [ _st.container() ]
    for i, opt in enumerate(options):
        display = format_func(opt)
        active  = _st.session_state[key] == opt
        col = cols[i] if horizontal else cols[0]

        style = (
            f"background:{color_map.get(opt,'#E2E2E2')};color:white;"
            if active and color_map else
            ("background:#E2E2E2;" if active else "background:#F5F5F5;")
        )

        with col:
            if _st.button(display, key=f"{key}_{i}", help=opt,
                        use_container_width=True,
                        type="secondary" if active else "primary"):
                _st.session_state[key] = opt

            # inject inline style (streamlit 1.32 adds data-testid=button)
            _st.markdown(
                f"""<style>
                div[data-testid="stButton"][data-key="{key}_{i}"] button {{ {style} }}
                </style>""",
                unsafe_allow_html=True)

    return _st.session_state[key]


# ─────────────────────────────────────────────────────────────────────
# 1. LOAD FULL DATA
# ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_5m(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["time"]    = pd.to_datetime(df["time"], utc=True)
    df["epoch"]   = (df["time"].astype("int64") // 10**9).astype(int)
    df["ny_date"] = df["time"].dt.tz_convert(NY).dt.date
    df["ny_time"] = df["time"].dt.tz_convert(NY).dt.time
    return df[["epoch", "open", "high", "low", "close", "ny_date", "ny_time"]]


@st.cache_data
def resample_frame(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    out = (
        df.set_index(pd.to_datetime(df["epoch"], unit="s", utc=True))
        .resample(rule, label="right", closed="right")
        .agg({"open": "first", "high": "max", "low": "min", "close": "last"})
        .dropna()
    )
    out["epoch"]   = (out.index.astype("int64") // 10**9).astype(int)
    out["ny_date"] = out.index.tz_convert(NY).date
    out["ny_time"] = out.index.tz_convert(NY).time
    return out.reset_index(drop=True)


full_raw = load_5m(PRICE_PATH)
full_15T = resample_frame(full_raw, "15T")
full_30T = resample_frame(full_raw, "30T")
full_1h  = resample_frame(full_raw, "1H")

# ─────────────────────────────────────────────────────────────────────
# 2. LEVEL TABLES
# ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_daily_levels(path: str) -> pd.DataFrame:
    lv = pd.read_csv(path)
    lv["date"] = pd.to_datetime(lv["analysis_date"]).dt.date
    return lv


@st.cache_data
def load_weekly_levels(path: str) -> pd.DataFrame:
    lv = pd.read_csv(path)
    tue = pd.to_datetime(lv["analysis_start_tuesday"]).dt.date
    lv["tuesday"] = tue

    wed_dt  = pd.to_datetime(tue + pd.to_timedelta(1, "D")) + pd.Timedelta(hours=8,  minutes=30)
    tueN_dt = pd.to_datetime(tue + pd.to_timedelta(7, "D")) + pd.Timedelta(hours=9,  minutes=30)

    wed_utc  = wed_dt.dt.tz_localize(NY).dt.tz_convert("UTC")
    tueN_utc = tueN_dt.dt.tz_localize(NY).dt.tz_convert("UTC")

    lv["start_epoch"] = (wed_utc.view("int64")  // 10**9).astype(int)
    lv["end_epoch"]   = (tueN_utc.view("int64") // 10**9).astype(int)
    return lv


daily_df  = load_daily_levels(LEVEL_PATH)
weekly_df = load_weekly_levels(WLEVEL_PATH)

# ─────────────────────────────────────────────────────────────────────
# 3. SIDEBAR

# Time‑frame selector ─ only the frames you already have
# time‑frame
with st.sidebar:
    # time‑frame pills (neutral grey)
    tf = pill_buttons(
        ["5 min", "15 min", "30 min", "1 h"],
        key="tf",
        index=1,
        container=st.sidebar,
    )

    # Daily / Weekly (neutral)
    lvl_kind = pill_buttons(
        ["Daily", "Weekly"],
        key="lvl",
        index=0,
        container=st.sidebar,
    )

    # Long / Short / Both (teal / red)
    side = pill_buttons(
        ["long", "short", "both"],
        key="side",
        index=0,
        colors={"long": "#26A69A", "short": "#EF5350"},
        container=st.sidebar,
    )






if lvl_kind == "Daily":
    N_days  = st.sidebar.slider("Trading days to show", 1, 20, 6)
    N_weeks = 6
else:
    N_weeks = st.sidebar.slider("Weekly windows to show", 1, 20, 6)
    N_days  = 6

# ─────────────────────────────────────────────────────────────────────
# 4. TRIM CANDLES
# ─────────────────────────────────────────────────────────────────────
base_df = {"5 min": full_raw, "15 min": full_15T,"30 min":full_30T, "1 h": full_1h}[tf]

if lvl_kind == "Daily":
    keep_dates = sorted(full_raw["ny_date"].unique())[-N_days:]
    df_view = base_df[base_df["ny_date"].isin(keep_dates)].copy()
    wk_subset, keep_weeks = None, None
else:
    keep_weeks = weekly_df.sort_values("tuesday")["tuesday"].unique()[-N_weeks:]
    wk_subset  = weekly_df[weekly_df["tuesday"].isin(keep_weeks)]
    first_ep   = int(wk_subset["start_epoch"].min())
    df_view    = base_df[base_df["epoch"] >= first_ep].copy()

# ─────────────────────────────────────────────────────────────────────
# 5. CANDLES
# ─────────────────────────────────────────────────────────────────────
bars = [
    {"time": int(r.epoch), "open": float(r.open), "high": float(r.high),
    "low": float(r.low),  "close": float(r.close)}
    for r in df_view.itertuples(index=False)
]
# after you create the `bars` list ───────────────────────────────────
total_bars = len(bars)

if lvl_kind == "Weekly":
    # find first bar that belongs to the *latest* weekly window
    last_week_start = int(wk_subset["start_epoch"].max())

    # idx_first_bar >= last_week_start
    first_idx = next(
        i for i, b in enumerate(bars)
        if b["time"] >= last_week_start
    )

    initial_from = first_idx                    # show full Wed→Tue span
    initial_to   = total_bars - 1
else:
    # Daily – keep your original “last 120 bars” view
    initial_from = max(total_bars - 120, 0)
    initial_to   = total_bars - 1


view_start, view_end = int(df_view["epoch"].iat[0]), int(df_view["epoch"].iat[-1])

# ─────────────────────────────────────────────────────────────────────
# 6. LEVEL SERIES  (with text markers)
# ─────────────────────────────────────────────────────────────────────
SESSION_START = datetime.time(9, 30)
SESSION_END   = datetime.time(15, 55)

cols_map = {
    "long":  ["high_20_level", "high_50_level", "high_80_level"],
    "short": ["low_20_level",  "low_50_level",  "low_80_level"],
}

label_map = {
    "high_20_level": "80%", "high_50_level": "50%", "high_80_level": "20%",
    "low_20_level":  "20%", "low_50_level":  "50%", "low_80_level":  "80%",
}

def style_for(side_: str):
    return {
        "color":   "#26A69A" if side_ == "long" else "#EF5350",
        "lineStyle": 0 if side_ == "long" else 2,   # solid vs dashed
    }

def make_line(first_ep: int, last_ep: int, val: float,
            label: str, side_: str) -> dict[str, Any]:
    sty = style_for(side_)
    return {
        "type": "Line",
        "data": [
            {"time": first_ep, "value": val},
            {"time": last_ep,  "value": val},
        ],
        "markers": [{
            "time": last_ep,
            "position": "inBar",
            "shape": "text",
            "text": label,
            "color": sty["color"],
            "size": 1,
        }],
        "options": {
            "priceScaleId": "right",
            "priceLineVisible": False,
            "lastValueVisible": False,
            "color": sty["color"],
            "lineWidth": 2,
            "lineStyle": sty["lineStyle"],
        },
    }

# ---------- builders use side_ arg instead of global ----------------
def daily_series(df_day_view: pd.DataFrame, side_: str):
    out: list[dict[str, Any]] = []
    mask = (df_day_view["ny_time"] >= SESSION_START) & (df_day_view["ny_time"] <= SESSION_END)
    if not mask.any():
        return out
    grp = df_day_view.loc[mask].groupby("ny_date")["epoch"].agg(["first", "last"]).reset_index()
    merged = grp.merge(daily_df, left_on="ny_date", right_on="date", how="left")

    for _, row in merged.iterrows():
        f_ep, l_ep = int(row["first"]), int(row["last"])
        for col in cols_map[side_]:
            v = row.get(col)
            if pd.notna(v):
                out.append(make_line(f_ep, l_ep, float(v), label_map[col], side_))
    return out

# cache key includes side_
if "wk_cache" not in st.session_state:
    st.session_state.wk_cache = {}

def weekly_series(v_start: int, v_end: int, side_: str):
    key = (tuple(keep_weeks), side_, v_start, v_end)
    cache = st.session_state.wk_cache
    if key in cache:
        return cache[key]

    df = wk_subset[
        (wk_subset["end_epoch"] >= v_start) & (wk_subset["start_epoch"] <= v_end)
    ]
    out: list[dict[str, Any]] = []
    for _, row in df.iterrows():
        r_start, r_end = int(row["start_epoch"]), int(row["end_epoch"])
        clip_start = max(r_start, v_start)
        clip_end   = min(r_end,   v_end)
        if clip_start == clip_end:
            clip_end += 60
        for col in cols_map[side_]:
            v = row.get(col)
            if pd.notna(v):
                out.append(make_line(clip_start, clip_end, float(v), label_map[col], side_))
    cache[key] = out
    return out

# ---------- choose which sides to draw ------------------------------
if side == "both":
    if lvl_kind == "Daily":
        level_series = (daily_series(df_view, "long") +
                        daily_series(df_view, "short"))
    else:
        level_series = (weekly_series(view_start, view_end, "long") +
                        weekly_series(view_start, view_end, "short"))
else:
    if lvl_kind == "Daily":
        level_series = daily_series(df_view, side)
    else:
        level_series = weekly_series(view_start, view_end, side)

# ─────────────────────────────────────────────────────────────────────
# 7. RENDER
# ─────────────────────────────────────────────────────────────────────
candlestick_series = {
    "type": "Candlestick",
    "data": bars,
    "options": {
        "priceScaleId": "right",
        "priceLineVisible": False,
        "upColor": "#26A69A",
        "downColor": "#EF5350",
        "wickUpColor": "#26A69A",
        "wickDownColor": "#EF5350",
        "borderUpColor": "#26A69A",
        "borderDownColor": "#EF5350",
    },
}

# ── chart_opts / chart_cfg patch ─────────────────────────────────────
chart_cfg = [{
    "chart": {
        "height": 900,
        "layout": {"background": {"color": "#0E1117"}, "textColor": "#D1D4DC"},
        "grid":   {"vertLines": {"color": "#2B3139"},
                   "horzLines": {"color": "#2B3139"}},

        "timeScale": {
            "rightOffset": 0,
            "visibleLogicalRange": {"from": initial_from, "to": initial_to},
            "secondsVisible": False,
            "tickMarkMaxCharacterLength": 5,
        },

        # ← NEW: tell LC to draw the axis strip on the right
        "rightPriceScale": {
            "visible": True,
            "borderVisible": True,
            "borderColor": "#444C55",   # thin divider line
            "ticksVisible": True,
        },
    },

    # remove / comment‑out the old "priceScales": {...} block
    # "priceScales": {...}

    "series": [candlestick_series, *level_series],
}]


renderLightweightCharts(cast(Any, chart_cfg), key="tsla_chart")


