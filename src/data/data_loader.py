import yfinance as yf
from pyspark.sql.functions import to_utc_timestamp, col

def load_stock_data(spark, ticker, period, interval):
    period_mapping = {
        "1D": "1d",
        "5D": "5d",
        "1M": "1mo",
        "3M": "3mo",
        "6M": "6mo",
        "1Y": "1y",
        "2Y": "2y",
        "5Y": "5y",
    }

    yf_period = period_mapping.get(period.upper())
    if not yf_period:
        raise ValueError(f"Invalid period: {period}")

    stock = yf.Ticker(ticker)
    
    pdf = stock.history(period=yf_period, interval=interval)
    pdf.reset_index(inplace=True)
    pdf.rename(columns={"Date": "Datetime"}, inplace=True)

    sdf = spark.createDataFrame(pdf)
    sdf = sdf.withColumn("Datetime", to_utc_timestamp(col("Datetime"), "US/Eastern"))

    return sdf, stock