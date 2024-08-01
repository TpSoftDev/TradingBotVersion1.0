################################################ TradingBotVersion1.0 ##################################################
import MetaTrader5 as mt
from datetime import datetime
from tabulate import tabulate
import pandas as pd
import plotly.express as px


def fetch_rates(ticker, interval, from_date, no_of_rows):
    """Fetch historical rates from MetaTrader 5."""
    rates = mt.copy_rates_from(ticker, interval, from_date, no_of_rows)
    headers = ['Date', 'Open', 'High', 'Low', 'Close']

    if rates.size > 0 and 'volume' in rates[0].dtype.names:
        headers.append('Volume')
        data = [[datetime.fromtimestamp(r['time']).strftime('%Y-%m-%d'),
                 r['open'], r['high'], r['low'], r['close'], r['volume']] for r in rates]
    else:
        data = [[datetime.fromtimestamp(r['time']).strftime('%Y-%m-%d'),
                 r['open'], r['high'], r['low'], r['close']] for r in rates]

    return data, headers


def display_account_info(account_info):
    """Display account information in a formatted table."""
    info_list = [
        ('Login', account_info.login),
        ('Trade Mode', account_info.trade_mode),
        ('Leverage', account_info.leverage),
        ('Limit Orders', account_info.limit_orders),
        ('Margin SO Mode', account_info.margin_so_mode),
        ('Trade Allowed', account_info.trade_allowed),
        ('Trade Expert', account_info.trade_expert),
        ('Margin Mode', account_info.margin_mode),
        ('Currency Digits', account_info.currency_digits),
        ('FIFO Close', account_info.fifo_close),
        ('Balance', account_info.balance),
        ('Credit', account_info.credit),
        ('Profit', account_info.profit),
        ('Equity', account_info.equity),
        ('Margin', account_info.margin),
        ('Margin Free', account_info.margin_free),
        ('Margin Level', account_info.margin_level),
        ('Margin SO Call', account_info.margin_so_call),
        ('Margin SO SO', account_info.margin_so_so),
        ('Margin Initial', account_info.margin_initial),
        ('Margin Maintenance', account_info.margin_maintenance),
        ('Assets', account_info.assets),
        ('Liabilities', account_info.liabilities),
        ('Commission Blocked', account_info.commission_blocked),
        ('Name', account_info.name),
        ('Server', account_info.server),
        ('Currency', account_info.currency),
        ('Company', account_info.company)
    ]
    return tabulate(info_list, headers=['Field', 'Value'], tablefmt='fancy_grid')


def fetch_and_plot_data(symbol, timeframe, start_date, end_date):
    """Fetch and plot OHLC data."""
    ohlc = pd.DataFrame(mt.copy_rates_range(symbol, timeframe, start_date, end_date))
    ohlc['time'] = pd.to_datetime(ohlc['time'], unit='s')
    #print(ohlc)
    fig = px.line(ohlc, x='time', y='close', title=f'{symbol} Close Price')
    fig.show()


def main():
    # Initialize MT5
    mt.initialize()
    mt.login(105098537, 'Cornw@ll246!', 'Trading.comMarkets-MT5')

    # Parameters for historical rates
    ticker = "EURUSD"
    interval = mt.TIMEFRAME_D1
    from_date = datetime.now()
    no_of_rows = 100

    # Fetch and display historical rates
    rates_data, rates_headers = fetch_rates(ticker, interval, from_date, no_of_rows)
    print(f"Historical Rates for {ticker}")
    print(tabulate(rates_data, headers=rates_headers, tablefmt='fancy_grid'))

    # Fetch and display account information
    account_info = mt.account_info()
    print("\nAccount Information:")
    print(display_account_info(account_info))

    # Parameters for OHLC data
    symbol = 'EURUSD'
    timeframe = mt.TIMEFRAME_W1
    start_date = datetime(2024, 7, 1)
    end_date = datetime.now()

    # Fetch and plot data
    fetch_and_plot_data(symbol, timeframe, start_date, end_date)


if __name__ == "__main__":
    main()