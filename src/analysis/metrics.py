import streamlit as st
from pyspark.sql.functions import sum, min, max

def display_stock_metrics(stock, data):
    previous_close = stock.info.get("previousClose", 0)
    open_price = data.select("Open").first()[0]
    volume = data.select(sum("Volume")).first()[0]
    day_range = f"{data.select(min('Low')).first()[0]:,.2f} - {data.select(max('High')).first()[0]:,.2f}"
    avg_volume = stock.info.get("averageVolume", 0)
    week52_range = f"{stock.info.get('fiftyTwoWeekLow', 0):,.2f} - {stock.info.get('fiftyTwoWeekHigh', 0):,.2f}"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Previous Close**")
        st.text(f"{previous_close:,.2f}")
    with col2:
        st.markdown("**Volume**")
        st.text(f"{volume:,.0f}")
    with col3:
        st.markdown("**52 Week Range**")
        st.text(f"{week52_range}")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("**Open**")
        st.text(f"{open_price:,.2f}")
    with col5:
        st.markdown("**Day's Range**")
        st.text(day_range)
    with col6:
        st.markdown("**Avg. Volume**")
        st.text(f"{avg_volume:,.0f}")
