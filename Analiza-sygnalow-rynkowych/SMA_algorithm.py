import csv
import pandas as pd
import os
import plotly.graph_objects as go


def get_nearest_trading_day(date, data):
    if date in data.index:
        return date
    else:
        previous_days = data.index[data.index < date]
        if not previous_days.empty:
            return previous_days[-1]
        else:
            # If no previous day is found, return the earliest available date
            return data.index[0]


def show_plot(data, i, short_trades, long_trades):
    fig = go.Figure()

    # Add the Candlestick trace
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Price'
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data[f'{i}-day SMA'],
        mode='lines',
        name=f'{i}-day SMA'
    ))

    # Plot the entry short signals
    fig.add_trace(go.Scatter(
        x=short_trades['Entry Date'],
        y=short_trades['Entry Price'],
        mode='markers',
        marker=dict(color='red', size=8),
        name='Entry Short Signal'
    ))

    # Plot the exit short signals
    fig.add_trace(go.Scatter(
        x=short_trades['Exit Date'],
        y=short_trades['Exit Price'],
        mode='markers',
        marker=dict(color='blue', size=8),
        name='Exit Short Signal'
    ))

    # Plot the entry long signals
    fig.add_trace(go.Scatter(
        x=long_trades['Entry Date'],
        y=long_trades['Entry Price'],
        mode='markers',
        marker=dict(color='green', size=8),
        name='Entry Long Signal'
    ))

    # Plot the exit long signals
    fig.add_trace(go.Scatter(
        x=long_trades['Exit Date'],
        y=long_trades['Exit Price'],
        mode='markers',
        marker=dict(color='orange', size=8),
        name='Exit Long Signal'
    ))

    shapes = []

    for _, trade in short_trades.iterrows():
        shapes.append(
            dict(
                type="rect",
                xref="x",
                yref="paper",
                x0=trade['Entry Date'],
                y0=0,
                x1=trade['Exit Date'],
                y1=1,
                fillcolor="rgba(255, 0, 0, 0.2)",
                line_width=0,
            )
        )

    for _, trade in long_trades.iterrows():
        shapes.append(
            dict(
                type="rect",
                xref="x",
                yref="paper",
                x0=trade['Entry Date'],
                y0=0,
                x1=trade['Exit Date'],
                y1=1,
                fillcolor="rgba(0, 255, 0, 0.2)",
                line_width=0,
            )
        )

    # Add rectangles to the layout
    fig.update_layout(
        title=f'Instrument price with {i}-day SMA, Entry and Exit Signals',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        shapes=shapes  # Add the shapes to the plot
    )

    fig.show()


def sma_algorithm(data,
                  i,
                  entry_short,
                  entry_long,
                  exit_short_threshold,
                  exit_long_threshold,
                  position_timeout,
                  multiple_entries,
                  capital_percent,
                  show,
                  save,
                  filename=None):
    # Calculate the i-day SMA and add it to the DataFrame
    data[f'{i}-day SMA'] = data['Adj Close'].rolling(window=i).mean()

    # Calculate the fair value
    data['fair_value'] = data['Adj Close'] / data[f'{i}-day SMA']

    # Identify entry short signals
    entry_short_signals = data[data['fair_value'] > entry_short]

    short_position_exit_date = None
    shorts_map = []

    for entry_short_date in entry_short_signals.index:
        if (not multiple_entries and
                short_position_exit_date is not None and
                short_position_exit_date > entry_short_date):
            continue

        next_exit = data[(data.index > entry_short_date) & (data['fair_value'] < exit_short_threshold)]

        if next_exit.empty:
            if position_timeout is not None:
                exit = get_nearest_trading_day(entry_short_date + position_timeout, data)
                shorts_map.append((entry_short_date, exit))
                short_position_exit_date = exit
                print(f"{entry_short_date} short timeout.")
                continue
            print(f"Couldn't find exit for {entry_short_date} short.")
            continue

        exit_signal = next_exit.iloc[0]
        shorts_map.append((entry_short_date, exit_signal.name))
        short_position_exit_date = exit_signal.name

    short_trades = pd.DataFrame(shorts_map, columns=['Entry Date', 'Exit Date'])

    # Calculate the returns for short trades
    short_trades['Entry Price'] = data.loc[short_trades['Entry Date'], 'Adj Close'].values
    short_trades['Exit Price'] = data.loc[short_trades['Exit Date'], 'Adj Close'].values
    short_trades['Return'] = (short_trades['Entry Price'] - short_trades['Exit Price']) / short_trades['Entry Price']
    short_trades['Position Type'] = 'Short'

    # Identify entry long signals
    entry_long_signals = data[data['fair_value'] < entry_long]

    # map - pairs <entry_date, exit_date>
    longs_map = []
    long_position_exit_date = None

    for entry_long_date in entry_long_signals.index:

        if not multiple_entries and long_position_exit_date is not None and long_position_exit_date > entry_long_date:
            continue

        next_exit = data[(data.index > entry_long_date) & (data['fair_value'] > exit_long_threshold)]

        if next_exit.empty:
            if position_timeout is not None:
                exit = get_nearest_trading_day(entry_long_date + position_timeout, data)
                longs_map.append((entry_long_date, exit))
                long_position_exit_date = exit
                print(f"{entry_long_date} long timeout.")
                continue
            print(f"Couldn't find exit for {entry_long_date} long.")
            continue

        exit_signal = next_exit.iloc[0]
        longs_map.append((entry_long_date, exit_signal.name))
        long_position_exit_date = exit_signal.name

    # Convert the lists to DataFrames for easier analysis
    long_trades = pd.DataFrame(longs_map, columns=['Entry Date', 'Exit Date'])

    # Calculate the returns for long trades
    long_trades['Entry Price'] = data.loc[long_trades['Entry Date'], 'Adj Close'].values
    long_trades['Exit Price'] = data.loc[long_trades['Exit Date'], 'Adj Close'].values
    long_trades['Return'] = (long_trades['Exit Price'] - long_trades['Entry Price']) / long_trades['Entry Price']
    long_trades['Position Type'] = 'Long'

    # Filter out empty DataFrames
    frames = [df for df in [short_trades, long_trades] if not df.empty]

    # Combine into one DataFrame if any DataFrame is not empty
    if frames:
        positions = pd.concat(frames, ignore_index=True)
        positions['Entry Date'] = pd.to_datetime(positions['Entry Date'])
        positions = positions.sort_values(by='Entry Date').reset_index(drop=True)
    else:
        print("No positions.")
        return

    balance = 1

    for r in positions['Return']:
        balance = capital_percent * balance * r + balance

    time_length = data.index[-1] - data.index[0]
    total_years = time_length.days / 365.25

    roi = 0

    if balance > 0:
        roi = (balance ** (1 / total_years) - 1) * 100

    # Calculate overall performance
    total_short_return = short_trades['Return'].sum()
    total_long_return = long_trades['Return'].sum()
    total_return = total_short_return + total_long_return

    print("\nTrades:")
    print(positions)

    print(f"\nTotal Short Return: {total_short_return:.2%}")
    print(f"Total Long Return: {total_long_return:.2%}")
    print(f"Total Return: {total_return:.2%}")
    print(f"Number of positions: {positions.shape[0]}")
    print(f"Balance: {balance:.2f}")
    print(f"ROI: {roi:.2f}%")

    file_exists = os.path.isfile(filename)

    if save:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "i",
                    "entry_short",
                    "entry_long",
                    "exit_short_threshold",
                    "exit_long_threshold",
                    "position_timeout",
                    "multiple_entries",
                    "capital_percent",
                    "total_short_return",
                    "total_long_return",
                    "total_return",
                    "positions",
                    "balance",
                    "roi"
                ])
                file.flush()

            writer.writerow([
                i,
                entry_short,
                entry_long,
                exit_short_threshold,
                exit_long_threshold,
                position_timeout,
                multiple_entries,
                capital_percent,
                total_short_return,
                total_long_return,
                total_return,
                positions.shape[0],
                balance,
                roi
            ])
            # Optionally, you can flush the buffer to ensure data is written immediately
            file.flush()
            print("Saved record.")
    if show:
        show_plot(data, i, short_trades, long_trades)


# Define the period for the SMA
i = 3  # Replace this with the desired number of days for the SMA
# These variables present current valuation based on moving average (fair value). fair = current / SMA
entry_short = 1.02  # Define the entry level for short
entry_long = 0.99  # Define the entry level for long
exit_short_threshold = 1.00  # Define the exit threshold for the short signal
exit_long_threshold = 1.02  # Define the exit threshold for the long signal
position_timeout = pd.to_timedelta(14, unit='D')  # max length of position in days
multiple_entries = True  # Set to True to allow multiple entries before exit
capital_percent = 0.3

show = True  # show plot
save = False  # save as csv file record
filename = 'SMA_algorithm_performance_BTCUSD_1d_ALL.csv'

# Load the data
data = pd.read_csv('GOLD_history.csv', index_col='Date', parse_dates=True)

data = data[(data.index > pd.Timestamp('2022-01-01')) & (data.index < pd.Timestamp('2023-01-01'))]
sma_algorithm(data,
                            i,
                            entry_short,
                            entry_long,
                            exit_short_threshold,
                            exit_long_threshold,
                            position_timeout,
                            multiple_entries,
                            capital_percent,
                            show,
                            save,
                            filename)


'''
for i in range(3,7):
    for entry_short in np.arange(1, 1.051, 0.01):
        for entry_long in np.arange(0.95, 1, 0.01):
            for exit_short_threshold in np.arange(0.95, 1, 0.01):
                for exit_long_threshold in np.arange(entry_long, 1.051, 0.01):
                    for capital_percent in np.arange(0.1, 1, 0.1):
                        SMA_algorithm.sma_algorithm(data,
                                                    i,
                                                    entry_short,
                                                    entry_long,
                                                    exit_short_threshold,
                                                    exit_long_threshold,
                                                    pd.to_timedelta(14, unit='D'),
                                                    True,
                                                    capital_percent,
                                                    show,
                                                    save,
                                                    filename)
                        SMA_algorithm.sma_algorithm(data,
                                                    i,
                                                    entry_short,
                                                    entry_long,
                                                    exit_short_threshold,
                                                    exit_long_threshold,
                                                    pd.to_timedelta(14, unit='D'),
                                                    False,
                                                    capital_percent,
                                                    show,
                                                    save,
                                                    filename)
                        print(i)

'''