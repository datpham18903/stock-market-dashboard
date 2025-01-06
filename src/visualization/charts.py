import numpy as np
import plotly.graph_objects as go
from tensorflow.keras.models import load_model
from analysis.technical_analysis import calculate_technical_indicators, prepare_prediction_data
from data.data_loader import load_stock_data


def create_stock_chart(
    spark, ticker, time_range="1D", chart_type="Line", indicators="MA50"
):
    interval_mapping = {
        "1D": "1m",
        "5D": "5m",
        "1M": "1h",
        "3M": "1d",
        "6M": "1d",
        "1Y": "1d",
        "2Y": "1wk",
        "5Y": "1wk",
    }

    dtick_mapping = {
        "1D": "900000",
        "5D": "H1",
        "1M": "D1",
        "3M": "M1",
        "6M": "M1",
        "1Y": "M1",
        "2Y": "M3",
        "5Y": "M3",
    }

    interval = interval_mapping.get(time_range, "1d")
    dtick_value = dtick_mapping.get(time_range, "D1")

    sdf, _ = load_stock_data(spark, ticker, time_range, interval)
    sdf = calculate_technical_indicators(sdf)
    x_test, scaler = prepare_prediction_data(sdf)

    model = load_model(
        "C:\Repositories\(Lab) Big Data Technology\stock-market-dashboard\src\model\Stock Predictions Model.keras"
    )
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    pdf = sdf.toPandas()
    fig = go.Figure()
    
    if pdf["Datetime"].dt.tz is None:
        pdf["Datetime"] = pdf["Datetime"].dt.tz_localize("US/Eastern")
        
    pdf = pdf.dropna(subset=["Close"])

    chart_types = {
        "Line": lambda: go.Scatter(
            x=pdf["Datetime"],
            y=pdf["Close"],
            name="Price",
            line=dict(color="#5992e3", width=1),
            connectgaps=False
        ),
        "Candlestick": lambda: go.Candlestick(
            x=pdf["Datetime"],
            open=pdf["Open"],
            high=pdf["High"],
            low=pdf["Low"],
            close=pdf["Close"],
            name="Price"
        ),
        "Baseline": lambda: go.Scatter(
            x=pdf["Datetime"],
            y=pdf["Close"],
            name="Price",
            fill="tonexty",
            line=dict(color="#5992e3", width=1),
            connectgaps=False
        ),
        "Mountain": lambda: go.Scatter(
            x=pdf["Datetime"],
            y=pdf["Close"],
            fill="tozeroy",
            name="Price",
            line=dict(color="#5992e3", width=1),
            connectgaps=False
        ),
        "Bar": lambda: go.Bar(
            x=pdf["Datetime"],
            y=pdf["Close"], 
            name="Price"
        )
    }

    fig.add_trace(chart_types[chart_type]())

    prediction_dates = pdf["Datetime"].iloc[-len(predictions) :]
    fig.add_trace(
        go.Scatter(
            x=prediction_dates,
            y=predictions.flatten(),
            name="Prediction",
            line=dict(color="green", dash="dash"),
            connectgaps=False
        )
    )

    fig.add_trace(
        go.Scatter(
            x=pdf["Datetime"],
            y=pdf[indicators],
            name=indicators,
            line=dict(color="#fb5f5f", width=1),
            connectgaps=False,
        )
    )
        
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=False),
            dtick=dtick_value,
            showgrid=True,
            gridcolor="#eeeeee"
        ),
        yaxis=dict(
            side="right", 
            showgrid=True, 
            gridcolor="#eeeeee"
        ),
        height=600,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(
            yanchor="top", 
            y=0.99, 
            xanchor="left", 
            x=0.05, 
            orientation="v"
        ),
        plot_bgcolor="white",
    )

    return fig
