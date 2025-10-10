import requests
import json
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Get your free API key from https://finnhub.io/
API_KEY = "d1cnshpr01qic6lesaa0d1cnshpr01qic6lesaag"

def get_stock_data(symbol):
    """Get stock data from Finnhub API"""
    
    base_url = "https://finnhub.io/api/v1"
    symbol = symbol.upper()
    
    try:
        stock_info = {}
        
        # Get Company Profile
        profile_url = f"{base_url}/stock/profile2"
        profile_params = {'symbol': symbol, 'token': API_KEY}
        profile_response = requests.get(profile_url, params=profile_params)
        
        if profile_response.status_code == 401:
            return {'error': 'Invalid API key. Please check your Finnhub API key.'}
        elif profile_response.status_code == 403:
            return {'error': 'API limit reached or invalid API key'}
        elif profile_response.status_code == 200:
            profile_data = profile_response.json()
            if profile_data:
                stock_info['company'] = {
                    'name': profile_data.get('name', 'N/A'),
                    'ticker': profile_data.get('ticker', 'N/A'),
                    'industry': profile_data.get('finnhubIndustry', 'N/A'),
                    'country': profile_data.get('country', 'N/A'),
                    'currency': profile_data.get('currency', 'N/A'),
                    'exchange': profile_data.get('exchange', 'N/A'),
                    'logo': profile_data.get('logo', ''),
                    'weburl': profile_data.get('weburl', '')
                }
            else:
                return {'error': 'Invalid stock symbol'}
        else:
            return {'error': f'API error: {profile_response.status_code}'}
        
        # Get Current Quote
        quote_url = f"{base_url}/quote"
        quote_params = {'symbol': symbol, 'token': API_KEY}
        quote_response = requests.get(quote_url, params=quote_params)
        
        if quote_response.status_code == 200:
            quote_data = quote_response.json()
            stock_info['quote'] = {
                'current_price': quote_data.get('c', 0),
                'change': quote_data.get('d', 0),
                'percent_change': quote_data.get('dp', 0),
                'high': quote_data.get('h', 0),
                'low': quote_data.get('l', 0),
                'open': quote_data.get('o', 0),
                'previous_close': quote_data.get('pc', 0)
            }
        
        # Get Basic Metrics
        metrics_url = f"{base_url}/stock/metric"
        metrics_params = {'symbol': symbol, 'metric': 'all', 'token': API_KEY}
        metrics_response = requests.get(metrics_url, params=metrics_params)
        
        if metrics_response.status_code == 200:
            metrics_data = metrics_response.json()
            if 'metric' in metrics_data:
                stock_info['metrics'] = {
                    '52_week_high': metrics_data['metric'].get('52WeekHigh', 'N/A'),
                    '52_week_low': metrics_data['metric'].get('52WeekLow', 'N/A'),
                    'market_cap': metrics_data['metric'].get('marketCapitalization', 'N/A'),
                    'pe_ratio': metrics_data['metric'].get('peBasicExclExtraTTM', 'N/A'),
                    'dividend_yield': metrics_data['metric'].get('dividendYieldIndicatedAnnual', 'N/A'),
                    'beta': metrics_data['metric'].get('beta', 'N/A')
                }
        
        return stock_info
        
    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Stock API</title>
    </head>
    <body>
        <h1>Stock Data API</h1>
        <p>Usage: /stock/&lt;symbol&gt;</p>
        <p>Example: <a href="/stock/AAPL">/stock/AAPL</a></p>
        <p>Test API Key: <a href="/test">/test</a></p>
    </body>
    </html>
    """

@app.route('/test')
def test_api():
    """Test if API key is working"""
    test_url = f"https://finnhub.io/api/v1/stock/profile2"
    test_params = {'symbol': 'AAPL', 'token': API_KEY}
    
    try:
        response = requests.get(test_url, params=test_params)
        if response.status_code == 200:
            return jsonify({'status': 'success', 'message': 'API key is valid'})
        elif response.status_code == 401:
            return jsonify({'status': 'error', 'message': 'Invalid API key'}), 401
        elif response.status_code == 403:
            return jsonify({'status': 'error', 'message': 'API limit reached or forbidden'}), 403
        else:
            return jsonify({'status': 'error', 'message': f'Status code: {response.status_code}'}), response.status_code
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/stock/<symbol>')
def stock_api(symbol):
    """API endpoint to get stock data"""
    stock_data = get_stock_data(symbol)
    response = make_response(jsonify(stock_data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Bonus: Get multiple stocks in parallel
def get_multiple_stocks():
    from concurrent.futures import ThreadPoolExecutor
    import time
    
    stocks = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
    
    print("Getting data for multiple stocks...")
    print("-" * 40)
    
    # Sequential processing
    start_time = time.time()
    results_sequential = []
    for stock in stocks:
        results_sequential.append(get_stock_data(stock))
    sequential_time = time.time() - start_time
    
    print(f"Sequential processing took: {sequential_time:.2f} seconds")
    
    # Parallel processing
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        results_parallel = list(executor.map(get_stock_data, stocks))
    parallel_time = time.time() - start_time
    
    print(f"Parallel processing took: {parallel_time:.2f} seconds")
    print(f"Speed improvement: {sequential_time/parallel_time:.1f}x faster!")
    
    # Print results
    print("\nStock Results:")
    print("-" * 40)
    for stock in results_parallel:
        if 'error' not in stock and 'company' in stock and 'quote' in stock:
            print(f"{stock['company']['name']}: ${stock['quote']['current_price']:.2f} ({stock['quote']['percent_change']:.2f}%)")

if __name__ == "__main__":
    print("Starting Stock API server...")
    print("Open index.html in your browser to use the frontend")
    print("API endpoint: http://localhost:5000/stock/<symbol>")
    print("-" * 40)
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  WARNING: You haven't added your Finnhub API key!")
        print("1. Get a free API key from: https://finnhub.io/")
        print("2. Replace 'YOUR_API_KEY_HERE' in app.py with your actual key")
        print("-" * 40)
    
    # Uncomment to test parallel processing
    # get_multiple_stocks()
    
    app.run(debug=True, port=5000)