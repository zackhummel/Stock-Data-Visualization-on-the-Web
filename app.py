import pygal, tempfile, webbrowser, os
from lxml import etree
from APIrequests import getRequestedSymbolData
from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy


#create a Flask object
app = Flask(__name__)

#allow the application to update while the server is running
app.config["DEBUG"] = True

#flash the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol']
        chart = int(request.form['chart_type'])
        time_series = int(request.form['time_series'])
        beginning_date = request.form['beginning_date']
        end_date = request.form['end_date']

        symbolData = getRequestedSymbolData(stock_symbol, time_series, beginning_date, end_date)

        labels = []
        opens, highs, lows, closes = [], [], [], []

        if isinstance(symbolData, dict):
            iterable = symbolData.items()
        else:
            iterable = symbolData

        for item in iterable:
            if isinstance(symbolData, dict):
                date, values = item
            else:
                date, values = item

            labels.append(date)
            opens.append(float(values['1. open']))
            highs.append(float(values['2. high']))
            lows.append(float(values['3. low']))
            closes.append(float(values['4. close']))

        create_chart(labels,opens,highs,lows,closes,chart,stock_symbol)

    return render_template('index.html')

def create_chart(labels,open,high,low,close,chart,stock_symbol):
    """
    Render a stock chart in the browser.

    Parameters:
        labels (list): Dates/timestamps from API
        values (list): Prices from API
        chart (str): 'line' or 'bar' (user input)
    """

    # Normalize input
    #chart = chart.lower()

    # Choose chart type
    if chart == 2:
        pygal_chart = pygal.Line(x_label_rotation=20)
    elif chart == 1:
        pygal_chart = pygal.Bar(x_label_rotation=20)
    else:
        raise ValueError("Invalid chart type. Choose 'line' or 'bar'.")

    # Add data
    pygal_chart.title = f"Stock Data for {stock_symbol} from {labels[-1]} to {labels[0]}"
    pygal_chart.x_labels = labels
    pygal_chart.add("Open", open)
    pygal_chart.add("High", high)
    pygal_chart.add("Low", low)
    pygal_chart.add("Close", close)



    return pygal_chart.render().decode("utf-8")

if __name__ == "__main__":
    app.run(debug=True)