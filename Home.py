import streamlit as st

st.title("NIFTY Stocks Analysis Dashboard")
st.markdown('<p style="font-size:20px;"><i>A lightweight, interactive dashboard to explore NIFTY sector trends and relative growth.</p>', unsafe_allow_html=True)

st.subheader("About")
st.markdown("""
<p style="font-size:17px;">
Welcome to my Stocks Analysis Dashboard!<br>
This is a tech demo that allows users to explore NIFTY sector data with interactive visualizations.<br>
The goal is to provide a simple, browser-based tool for comparing sector performance and analyzing historical trends.
</p>
""", unsafe_allow_html=True)

st.subheader("Features")
st.markdown("""
<ul style="font-size:17px;">
<li>Dynamic candlestick charts for NIFTY sectors</li>
<li>Toggleable data analysis tools for deeper insights</li>
<li>Relative Growth Analysis Chart to compare multiple sectors across years</li>
<li>Easy navigation using the sidebar</li>
</ul>
""", unsafe_allow_html=True)


st.subheader("Coming Soon")
st.markdown("""
<ul style="font-size:18px;">
<li>Additional technical indicators (RSI, MACD)</li>
<li>Sector-specific case studies and advanced analytics</li>
<li>Major dates where the market shifted prominently marked on graphs</li>
</ul>
""", unsafe_allow_html=True)

st.markdown("""
<p style="font-size:18px;"><i>
Use the sidebar to navigate between different pages and analyses. Feedback and suggestions are welcome!
</p>
""", unsafe_allow_html=True)
