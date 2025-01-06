import streamlit as st
import yfinance as yf
from core.config import init_spark
from core.utils import get_market_close_string
from data.data_loader import load_stock_data
from analysis.metrics import display_stock_metrics
from visualization.charts import create_stock_chart
from visualization.styles import align_row_elements

def main():
    spark = init_spark()
    
    st.set_page_config(page_title="Stock Dashboard Application", page_icon=":chart_with_upwards_trend:", layout="wide")
    st.markdown(f"<style>{align_row_elements()}</style>", unsafe_allow_html=True)

    ticker = st.text_input("", value="TSLA", placeholder="Search for symbols")

    if ticker:
        try:
            stock = yf.Ticker(ticker)
            company = stock.info.get("longName")

            if company:
                st.title(f"{company} ({ticker})")

                data = stock.history(period="1d")
                closing_price = data["Close"].iloc[-1]
                previous_closing_price = stock.info.get("previousClose")
                change = closing_price - previous_closing_price
                percentage_change = (change / previous_closing_price) * 100
                currency = stock.info.get("currency")

                col1 = st.columns(1)[0]
                col1.metric(
                    label="",
                    value=f"{closing_price:,.2f} ({currency})",
                    delta=f"{change:,.2f} ({percentage_change:,.2f}%)",
                )
                col1.caption(get_market_close_string())

                col_config = [
                    0.0216,
                    0.0216,
                    0.0222,
                    0.0221,
                    0.0244,
                    0.0204,
                    0.0202,
                    0.25,
                    0.1,
                    0.1,
                ]
                cols = st.columns(col_config)

                buttons = ["1D", "5D", "1M", "3M", "6M", "1Y", "2Y", "5Y"]
                if "time_range" not in st.session_state:
                    st.session_state.time_range = "1D"

                for i, col in enumerate(cols[:8]):
                    if col.button(buttons[i]):
                        st.session_state.time_range = buttons[i]

                indicators = cols[8].selectbox(
                    "", ["MA50", "MA100", "MA200"], label_visibility="collapsed"
                )

                chart_type = cols[9].selectbox(
                    "",
                    ["Line", "Candlestick", "Baseline", "Mountain", "Bar"],
                    label_visibility="collapsed",
                )

                fig = create_stock_chart(
                    spark, ticker, st.session_state.time_range, chart_type, indicators
                )
                st.plotly_chart(fig, use_container_width=True)

                sdf, _ = load_stock_data(spark, ticker, "1d", "1m")
                display_stock_metrics(stock, sdf)

            else:
                st.error("Invalid symbol. Please try again.")

        except Exception as e:
            st.error(f"Error loading data: {e}")


if __name__ == "__main__":
    main()