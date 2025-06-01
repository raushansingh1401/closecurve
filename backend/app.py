from flask import Flask, request, jsonify
import yfinance as yf
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/average-close')
def average_close():
    ticker = request.args.get('ticker')
    year = request.args.get('year')
    month = request.args.get('month')

    if not ticker or not year or not month:
        return jsonify({'error': 'Please provide ticker, year, and month'}), 400

    try:
        year = int(year)
        month = int(month)

        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        print(f"Fetching {ticker} from {start_date} to {end_date}")
        data = yf.download(ticker, start=start_date, end=end_date)

        if data.empty:
            return jsonify({'error': 'No data found for the given ticker/month'}), 404

        print("TYPE of data:", type(data))
        print("COLUMNS in data:", data.columns)
        print("DATA HEAD:\n", data.head())

        # Access the correct Series using MultiIndex
        close_series = data[('Close', ticker.upper())]

        print("TYPE of Close:", type(close_series))
        print("Closing prices:", close_series.tolist())

        avg_close = round(close_series.mean(), 2)

        return jsonify({
            'ticker': ticker.upper(),
            'average_close': avg_close
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

