import random, os

from flask import Flask, jsonify, make_response, render_template, request, send_from_directory, redirect, url_for
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired

from model import SpotTrade
from service import CryptoService
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '9bda71c7b88e4a60a0c9c8d1abbeef7e'

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


@app.route("/api/v1/dashboard/<string:pname>", methods=['GET'])
def api_dashboard(pname):
    spot_view = CryptoService.get_spot_view(pname)
    return jsonify(spot_view.to_dict())

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


# Route for adding a new item
@app.route('/add_spot', methods=['GET', 'POST'])
def add_spot():
    form = SpotTradeForm()
    if form.validate_on_submit():
        new_item = SpotTrade.SpotTrade(id=None, coin_marketcap_id=None, symbol=form.symbol.data, buy_price=form.buyPrice.data, quantity=form.qty.data, logo=None, portfolioId=form.portfolioId.data)
        #db.session.add(new_item)
        #db.session.commit()
        CryptoService.save_spot_trade(new_item)
        #flash('Item added successfully!', 'success')
        #return redirect(url_for('edit_spot', spot_id=new_item.id))
        return redirect(url_for('add_spot'))

    return render_template('add_spot.html', form=form)


@app.route('/edit_spot/<string:spot_id>', methods=['GET', 'POST'])
def edit_spot(spot_id):
    # Fetch the item from the database
    item = CryptoService.get_spot_trade(spot_id)
    form = SpotTradeForm(obj=item)  # Populate form with existing data

    if form.validate_on_submit():
        # Update the item's details
        #item.symbol = form.symbol.data
        item.buy_price = form.buyPrice.data
        item.quantity = form.qty.data

        CryptoService.save_spot_trade(item)
        #db.session.commit()
        #flash('Item updated successfully!', 'success')
        return redirect(url_for('edit_spot', spot_id=item.id))  # Redirect to edit page

    return render_template('edit_spot.html', form=form, item=item)

class SpotTradeForm(FlaskForm):
    portfolioId = StringField('Portfolio Id', validators=[DataRequired()])
    symbol = StringField('Symbol', validators=[DataRequired()])
    buyPrice = StringField('Buy Price', validators=[DataRequired()])
    qty = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')
