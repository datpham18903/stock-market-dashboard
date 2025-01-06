# Stock Dashboard Application

A real-time stock market dashboard built with Streamlit, PySpark, and machine learning capabilities.

## Features

- Real-time stock price tracking
- Interactive charts with multiple visualization options:
  - Line chart
  - Candlestick chart
  - Baseline chart
  - Mountain chart
  - Bar chart
- Technical indicators:
  - 50-day moving average
  - 100-day moving average
  - 200-day moving average
- Machine learning-based price predictions
- Market metrics and statistics
- Responsive design

## Prerequisites

- Python 3.10+
- Java JDK 11
- Apache Spark 3.5.4
- Git

## Environment Setup

1. Set up Java and Spark:
```bash
# Set environment variables
export JAVA_HOME="C:\Program Files\Java\jdk-11"
export SPARK_HOME="C:\spark\spark-3.5.4-bin-hadoop3"
export PATH="$JAVA_HOME/bin:$PATH"
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-market-dashboard.git
cd stock-market-dashboard
```

3. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Unix/macOS
venv\Scripts\activate  # For Windows
```

4. Install dependencies:
```bash
pip install -r src/requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
cd src
streamlit run app.py
```

2. Open your browser and navigate to: http://localhost:8501

3. Enter a stock symbol (e.g., TSLA) in the search box

4. Explore different chart types and technical indicators using the interface

## Contributing

1. Fork the repository

2. Create your feature branch (git checkout -b feature/amazing-feature)

3. Commit your changes (git commit -m 'Add some amazing feature')

4. Push to the branch (git push origin feature/amazing-feature)

5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

- Streamlit for the web framework
- Apache Spark for data processing
- yfinance for stock data
- Plotly for interactive charts
- TensorFlow for machine learning capabilities
