import pygal
from lxml import etree
import tempfile
import webbrowser
import os


def user_input():
    stock_symbol = input("Stock Symbol: ")
    chart = input("Which chart would you like: ")
    time_series = input("Which time series function: ")
    beginning_date = input("Beginning date: ")
    end_date = input("End date: ")
    return stock_symbol, chart, time_series, beginning_date, end_date

def create_chart(labels, values, chart):
    """
    Render a stock chart in the browser.

    Parameters:
        labels (list): Dates/timestamps from API
        values (list): Prices from API
        chart (str): 'line' or 'bar' (user input)
    """

    # Normalize input
    chart = chart.lower()

    # Choose chart type
    if chart == "line":
        pygal_chart = pygal.Line(x_label_rotation=20)
    elif chart == "bar":
        pygal_chart = pygal.Bar(x_label_rotation=20)
    else:
        raise ValueError("Invalid chart type. Choose 'line' or 'bar'.")

    # Add data
    pygal_chart.title = "Stock Data"
    pygal_chart.x_labels = labels
    pygal_chart.add("Price", values)

    # Render SVG
    svg_data = pygal_chart.render()

    # Wrap in HTML
    html = etree.Element("html")
    body = etree.SubElement(html, "body")
    body.append(etree.fromstring(svg_data))

    # Save and open in browser
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    tmp_file.write(etree.tostring(html, pretty_print=True, method="html"))
    tmp_file.close()

    webbrowser.open(f"file://{os.path.abspath(tmp_file.name)}")
def main():
    stock_symbol, chart, time_series, beginning_date, end_date = user_input()


main()