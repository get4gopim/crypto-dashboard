import random, os

from flask import Flask, jsonify, make_response, render_template, request, send_from_directory
from service import CryptoService

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Function to generate random colors
def generate_colors(num_colors):
    colors = []
    for _ in range(num_colors):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        colors.append(f"rgba({r}, {g}, {b}, 0.6)")  # For backgroundColor
    return colors

@app.route("/<string:pname>", methods=['GET'])
def spot_view(pname):
    spot_view = CryptoService.get_spot_view(pname)
    labels = []
    data_values = []
    background_colors = []
    border_colors = []
    portfolio = CryptoService.get_portfolio(pname)
    if spot_view is not None:
        # Define Plot Data
        labels = [spot_order.symbol for spot_order in spot_view.spot_orders]
        data_values = [spot_order.est_cost for spot_order in spot_view.spot_orders]
        # Generate random colors
        background_colors = generate_colors(len(labels))
        border_colors = [color.replace("0.6", "1") for color in background_colors]

    return render_template('index.html',
                           spot_view=spot_view, labels=labels, data_values=data_values,
                           background_colors=background_colors, border_colors=border_colors, portfolio=portfolio)



@app.route('/dashboard', methods=['GET'])
def index():
    # Example data for the dashboard
    return render_template('dashboard.html')


@app.route("/meta_data")
def meta_data():
    # Get the 'q' parameter from the query string
    cid = request.args.get('cid')
    meta_data = CryptoService.get_meta_data(cid)
    return render_template('meta_data.html', meta_data=meta_data)

@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
