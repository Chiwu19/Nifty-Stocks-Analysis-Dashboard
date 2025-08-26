import streamlit as st
import pandas as pd
import time
import datetime
from streamlit_lightweight_charts import renderLightweightCharts

st.set_page_config(page_title="NIFTY Dashboard", layout="wide")

st.markdown(
    """
    <style>
        .block-container {
            max-width: 90%;   /* increase to 100% for full screen */
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

NIFTY_50 = load_csv('NIFTY CSV/Nifty 50 Historical Data.csv')
NIFTY_IT = load_csv('NIFTY CSV/Nifty IT Historical Data.csv')
NIFTY_BANK = load_csv('NIFTY CSV/Nifty Bank Historical Data.csv')
NIFTY_FMCG = load_csv('NIFTY CSV/Nifty FMCG Historical Data.csv')
NIFTY_PHARMA = load_csv('NIFTY CSV/Nifty Pharma Historical Data.csv')

NIFTY_50.columns = ['date','close','open','high','low','volume','Change%']
NIFTY_IT.columns = ['date','close','open','high','low','volume','Change%']
NIFTY_BANK.columns = ['date','close','open','high','low','volume','Change%']
NIFTY_FMCG.columns = ['date','close','open','high','low','volume','Change%']
NIFTY_PHARMA.columns = ['date','close','open','high','low','volume','Change%']


NIFTY_FMCG = NIFTY_FMCG.drop(3600)

NIFTY_PHARMA = NIFTY_PHARMA.drop(3600)

NIFTY_50.drop(NIFTY_50.index[3600:4865], inplace=True)

NIFTY_BANK.drop(NIFTY_BANK.index[3600:4865], inplace=True)

NIFTY_IT.drop(NIFTY_IT.index[3600:4861], inplace=True)

stocks = {
    "NIFTY 50": NIFTY_50,
    "NIFTY IT": NIFTY_IT,
    "NIFTY BANK": NIFTY_BANK,
    "NIFTY FMCG": NIFTY_FMCG,
    "NIFTY PHARMA": NIFTY_PHARMA
}

def parse_number(x):
    if isinstance(x, str):
        if 'M' in x:
            return float(x.replace('M','')) * 1e6
        elif 'B' in x:
            return float(x.replace('B','')) * 1e9
        elif 'K' in x:
            return float(x.replace('K','')) * 1e3
        else:
            return float(x.replace(',', ''))
    return x

# Remove commas and convert to float
NIFTY_50['close'] = NIFTY_50['close'].str.replace(',', '').astype(float)
NIFTY_IT['close'] = NIFTY_IT['close'].str.replace(',', '').astype(float)
NIFTY_BANK['close'] = NIFTY_BANK['close'].str.replace(',', '').astype(float)
NIFTY_FMCG['close'] = NIFTY_FMCG['close'].str.replace(',', '').astype(float)
NIFTY_PHARMA['close'] = NIFTY_PHARMA['close'].str.replace(',', '').astype(float)

NIFTY_50['volume'] = NIFTY_50['volume'].apply(parse_number)
NIFTY_IT['volume'] = NIFTY_IT['volume'].apply(parse_number)
NIFTY_BANK['volume'] = NIFTY_BANK['volume'].apply(parse_number)
NIFTY_FMCG['volume'] = NIFTY_FMCG['volume'].apply(parse_number)
NIFTY_PHARMA['volume'] = NIFTY_PHARMA['volume'].apply(parse_number)

for df in stocks.values():
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    df.reset_index(drop=True, inplace=True)

for df in [NIFTY_50, NIFTY_IT, NIFTY_BANK, NIFTY_FMCG, NIFTY_PHARMA]:
    for col in ['open', 'high', 'low', 'close']:
        df[col] = df[col].astype(str).str.replace(',', '').astype(float)
    df['volume'] = df['volume'].apply(parse_number)

st.title("NIFTY STOCK ANALYSIS")
tab1, tab2 = st.tabs(["📈 Stock Candlestick", "📊 Relative Indices"])

with tab1:
    st.header("Stock Overview:")
    stock_name = st.selectbox("Select Stock", list(stocks.keys()))
    df = stocks[stock_name]
    df['date'] = pd.to_datetime(df['date'])

    min_date, max_date = df['date'].min(), df['date'].max()

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From date", min_value=min_date, max_value=max_date, value=min_date)
    with col2:
        end_date = st.date_input("To date", min_value=min_date, max_value=max_date, value=max_date)

    if start_date > end_date:
        st.error("⚠️ 'From date' must be before 'To date'")
    else:
        df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]


    st.subheader("Chart Options")
   
    chart_options = st.pills(
        "Chart Options",
        ["20-day MA", "50-day MA", "200-day MA", "Volume"],
        selection_mode="multi",
        default=["Volume"]  # default selections
    )

    show_ma20 = "20-day MA" in chart_options
    show_ma50 = "50-day MA" in chart_options
    show_ma200 = "200-day MA" in chart_options
    show_volume = "Volume" in chart_options

    ohlc_data = [
        {
            "time": row["date"].strftime("%Y-%m-%d"),
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["close"]
        }
        for _, row in df.iterrows()
    ]

    df['volume'] = df['volume'].fillna(0)  # replace NaN with 0
    df['volume'] = df['volume'].astype(float)

    volume_data = [
    {
        "time": row["date"].strftime("%Y-%m-%d"),
        "value": row["volume"],
        "color": "rgba(38, 166, 154, 0.2)" if row["close"] >= row["open"] else "rgba(239, 83, 80, 0.2)",
    }
    for _, row in df.iterrows()
    ]


    chart_options = {
        "height": 500,
        "layout": {
            "background": {"type": "solid", "color": "black"},
            "textColor": "#d1d4dc",
        },
        "grid": {
            "vertLines": {
                "color": 'rgba(42, 46, 57, 0)',
            },
            "horzLines": {
                "color": 'rgba(42, 46, 57, 0)',
            }
        },
        "borderColor": 'black',
        "borderVisible": True
    }

    series = [
        {
            "type": "Candlestick",
            "data": ohlc_data,
            "options": {"upColor": "green", "downColor": "red"}
        }
    ]

    if show_volume:
        series.append({
            "type": "Histogram",
            "data": volume_data,
            "options": {"priceScaleId": "", "priceFormat": {"type": "volume"}}
        })

    if show_ma20:
        df["MA20"] = df["close"].rolling(window=20).mean()
        ma20 = [{"time": row["date"].strftime("%Y-%m-%d"), "value": row["MA20"]}
                for _, row in df.dropna(subset=["MA20"]).iterrows()]
        series.append({
            "type": "Line",
            "data": ma20,
            "options": {"color": "blue", "lineWidth": 1}
        })

    if show_ma50:
        df["MA50"] = df["close"].rolling(window=50).mean()
        ma50 = [{"time": row["date"].strftime("%Y-%m-%d"), "value": row["MA50"]}
                for _, row in df.dropna(subset=["MA50"]).iterrows()]
        series.append({
            "type": "Line",
            "data": ma50,
            "options": {"color": "orange", "lineWidth": 1}
        })

    if show_ma200:
        df["MA200"] = df["close"].rolling(window=200).mean()
        ma200 = [{"time": row["date"].strftime("%Y-%m-%d"), "value": row["MA200"]}
                for _, row in df.dropna(subset=["MA200"]).iterrows()]
        series.append({
            "type": "Line",
            "data": ma200,
            "options": {"color": "red", "lineWidth": 1}
        })

    important_dates = ["2020-03-24"]

    max_value = df['high'].max()
    min_value = df['low'].min()

    for date in important_dates:
        ts = date.strftime("%Y-%m-%d") if isinstance(date, pd.Timestamp) else date
        series.append({
            "type": "Line",
            "data": [
                {"time": ts, "value": min_value},  # bottom
                {"time": ts, "value": max_value}   # top
            ],
            "options": {"color": "rgba(255,0,0,0.3)", "lineWidth": 1}
        })    

    renderLightweightCharts(
        [{
            "chart": chart_options,
            "series": series
        }],
        key="candlestick_chart"
    )


@st.cache_data
def compute_relative_performance():
    y1_norm = (NIFTY_50['close'] / NIFTY_50['close'].iloc[0] - 1) * 100
    y2_norm = (NIFTY_IT['close'] / NIFTY_IT['close'].iloc[0] - 1) * 100
    y3_norm = (NIFTY_BANK['close'] / NIFTY_BANK['close'].iloc[0] - 1) * 100
    y4_norm = (NIFTY_FMCG['close'] / NIFTY_FMCG['close'].iloc[0] - 1) * 100
    y5_norm = (NIFTY_PHARMA['close'] / NIFTY_PHARMA['close'].iloc[0] - 1) * 100
    return y1_norm, y2_norm, y3_norm, y4_norm, y5_norm

with tab2:


    st.header("Relative Performance of Indices")


    min_date, max_date = NIFTY_50['date'].min(), NIFTY_50['date'].max()
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From date", min_value=min_date, max_value=max_date, value=min_date, key="rel_from_date")
        
    with col2:
        end_date = st.date_input("To date", min_value=min_date, max_value=max_date, value=max_date, key="rel_to_date")

    if start_date > end_date:
        st.error("⚠️ 'From date' must be before 'To date'")
    else:

        dfs = {}
        for k, v in stocks.items():
            dfs[k] = v[(v['date'] >= pd.to_datetime(start_date)) & (v['date'] <= pd.to_datetime(end_date))].copy()


        for k, v in dfs.items():
            base = v['close'].iloc[0]
            dfs[k]['growth'] = (v['close'] / base - 1) * 100   # percentage growth vs start


        selected = st.pills(
            "Pick sectors to compare:",
            list(stocks.keys()),
            selection_mode="multi",
            default=["NIFTY 50"]
        )


        chart_options = {
            "height": 500,
            "layout": {
                "background": {"type": "solid", "color": "black"},
                "textColor": "#d1d4dc",
            },
            "grid": {
                "vertLines": {"color": 'rgba(42, 46, 57, 0)'},
                "horzLines": {"color": 'rgba(42, 46, 57, 0)'},
            },
            "crosshair": {"mode": 0},
            "rightPriceScale": {"visible": True},
            "timeScale": {"timeVisible": True, "secondsVisible": False},
        }


        colors = {
            "NIFTY 50": "yellow",
            "NIFTY IT": "cyan",
            "NIFTY BANK": "orange",
            "NIFTY FMCG": "violet",
            "NIFTY PHARMA": "lime",
        }

        legend_str = " | ".join(
        f"<span style='color:{colors.get(idx, 'white')}; font-weight:bold;'>{idx}</span>"
        for idx in selected
        )
        st.markdown(legend_str, unsafe_allow_html=True)

        series = []
        for idx in selected:
            sdata = [
                {"time": row["date"].strftime("%Y-%m-%d"), "value": row["growth"]}
                for _, row in dfs[idx].iterrows()
            ]
            series.append({
                "type": "Line",
                "data": sdata,
                "options": {"color": colors.get(idx, "white"), "lineWidth": 2},
                "legend": idx,
            })


        renderLightweightCharts(
            [{
                "chart": chart_options,
                "series": series
            }],
            key="relative_chart"
        )
        
        