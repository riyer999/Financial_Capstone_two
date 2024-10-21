from flask import Flask, jsonify, render_template
import yfinance as yf

app = Flask(__name__)

# List of Sector ETFs
sector_etfs = ['XLK', 'XLF', 'XLY', 'XLV', 'XLE', 'XLU', 'XLI', 'XLB', 'XLRE', 'XLC', 'XLP']


@app.route('/')
def home():
    return render_template('index.html')  # Ensure this HTML file exists in the templates folder


@app.route('/api/sector_data', methods=['GET'])
def get_sector_data():
    etf_metrics = {}

    for etf in sector_etfs:
        ticker = yf.Ticker(etf)
        info = ticker.info

        total_assets = info.get('totalAssets', 0)
        name = info.get('longName', 'N/A')

        etf_metrics[etf] = {
            'name': name,
            'total_assets': total_assets
        }

    return jsonify(etf_metrics)


if __name__ == '__main__':
    app.run(debug=True)
