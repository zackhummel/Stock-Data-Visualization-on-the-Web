import pygal, tempfile, webbrowser, os
from lxml import etree
from APIrequests import getRequestedSymbolData


def user_input():

    try: 
        stock_symbol = input("Enter the Stock Symbol you are looking for: ")

        print("\nChart Types\n------------")
        print("1. Bar\n2. Line")
        chart = int(input("Which chart type would you like? (1, 2): "))

        print("\nSelect Time Series\n------------")
        print("1. Intraday\n2. Daily\n3. Weekly\n4. Monthly")
        time_series = int(input("Which time series function (1, 2, 3, 4): "))


        beginning_date = input("\nBeginning date (YYYY-MM-DD): ")


        end_date = input("End date (YYYY-MM-DD): ")

    except Exception as e:
        print(f"Something went wrong.\n{e}")


    return stock_symbol, chart, time_series, beginning_date, end_date

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
    pygal_chart.title = f"Stock Data for {stock_symbol} from {labels[-1]} to {labels[1]}"
    pygal_chart.x_labels = labels
    pygal_chart.add("Open", open)
    pygal_chart.add("High", high)
    pygal_chart.add("Low", low)
    pygal_chart.add("Close", close)

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
    print("\nStock Data Visualizer\n--------------------------------")
    stock_symbol, chart, time_series, beginning_date, end_date = user_input()
    #Remove this when API works
    print(getRequestedSymbolData(stock_symbol, time_series, beginning_date, end_date))

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

if __name__ == "__main__":
    main()