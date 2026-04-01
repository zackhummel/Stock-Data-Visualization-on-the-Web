def user_input():
    stock_symbol = input("Stock Symbol: ")
    chart = input("Which chart would you like: ")
    time_series = input("Which time series function: ")
    beginning_date = input("Beginning date: ")
    end_date = input("End date: ")
    return stock_symbol, chart, time_series, beginning_date, end_date
def main():
    stock_symbol, chart, time_series, beginning_date, end_date = user_input()

main()