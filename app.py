import pygal, tempfile, webbrowser, os
from lxml import etree
from APIrequests import getRequestedSymbolData


def user_input():

    try: 
        stock_symbol = input("Stock Symbol: ")

        print("Chart Types\n------------")
        print("1. Bar\n2. Line")
        chart = int(input("Which chart would you like (1, 2): "))

        print("Select Time Series\n------------")
        print("1. Intraday\n2. Daily\n3. Weekly\n4. Monthly")
        time_series = int(input("Which time series function (1, 2, 3, 4): "))


        beginning_date = input("Beginning date (YYYY-MM-DD): ")


        end_date = input("End date (YYYY-MM-DD): ")

    except Exception as e:
        print(f"Something went wrong.\n{e}")


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
    #chart = chart.lower()

    # Choose chart type
    if chart == 2:
        pygal_chart = pygal.Line(x_label_rotation=20)
    elif chart == 1:
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
    print("Stock Data Visualizer\n--------------------------------")
    stock_symbol, chart, time_series, beginning_date, end_date = user_input()
    
    print(getRequestedSymbolData(stock_symbol, time_series, beginning_date, end_date))


if __name__ == "__main__":
    main()