import numpy as np
import random
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


def resample_to_month_using_end(series):
    def end_month(array_like):
        return array_like[-1]
    return series.resample('1M').apply(end_month)


def resample_integrate_to_month(series):
    def integrate_month(array_like):
        return np.sum(array_like)
    return series.resample('1M').apply(integrate_month)


def sample_date_from_rectangular(date_range: pd.date_range, size: int=None):

    length = len(date_range)
    index = random.randint(0, length - 1)

    return date_range[index]


def sample_from_normal(mean: float, deviation: float, size: int=None):

    return np.random.normal(loc=mean, scale=deviation, size=size)


def generate_randn_event_rect_norm(
        *, dates,
        start_date,
        mean,
        end_date=None,
        deviation: float=0.0,
        name: str='',
        odds: float=1.0):

    if end_date is None:
        end_date = start_date + pd.DateOffset(days=1)

    date_deviation = pd.date_range(
        freq='D',
        start=start_date,
        end=end_date
    )

    event_date = sample_date_from_rectangular(date_deviation)

    did_happen = (int(random.random() <= odds))

    if deviation < 0.0:
        raise ValueError('Error, negative deviation')

    if deviation == 0.0:
        event_value = mean * did_happen
    else:
        event_value = sample_from_normal(mean, deviation) * did_happen

    values = np.zeros((len(dates), ))
    index = dates.get_loc(event_date, method='nearest')

    if index >= 0 and index < len(values):
        values[index] = int(event_value)

    cash_flow = pd.Series(values, index=dates, name=name)

    return cash_flow


def generate_monthly_randn_norm_event(
        dates,
        pay_day_of_month: int,
        mean,
        deviation,
        name: str):

    event_value = sample_from_normal(mean, deviation)
    values = np.zeros((len(dates), ))
    index = 0

    for date in dates:
        if date.day == pay_day_of_month:
            values[index] = int(event_value)
        index += 1

    return pd.Series(values, index=dates, name=name)


def generate_payroll_line(
        dates,
        amount: int,
        pay_day_of_month: int=25,
        name: str=''):

    values = np.zeros((len(dates), ))
    index = 0

    for date in dates:
        if date.day == pay_day_of_month:
            values[index] = -int(amount)
        index += 1

    return pd.Series(values, index=dates, name=name)


def plot_cash_series(cash_series, dates):

    months = mdates.MonthLocator()  # every month
    month_fmt = mdates.DateFormatter('%b')

    # Load a numpy structured array from yahoo csv data with fields date, open,
    # close, volume, adj_close from the mpl-data/example directory.  This array
    # stores the date as an np.datetime64 with a day unit ('D') in the 'date'
    # column.

    fig, ax = plt.subplots()

    for cash in cash_series:

        c_idx = 0
        for j in range(len(cash)):
            if cash[j] < 0:
                print(f'Insolvency by {dates[j]}')
                c_idx = j
                break

        if c_idx > 0:
            if c_idx < 2:
                # Immediately insolvent
                ax.plot(dates, cash, linewidth=2, alpha=0.2, color='r')
            else:
                ax.plot(dates[0:c_idx], cash[0:c_idx],
                        linewidth=2, alpha=0.2, color='g')
                ax.plot(dates[c_idx - 1:-1], cash[c_idx - 1:-1],
                        linewidth=2, alpha=0.2, color='r')
        else:
            # Fully solvent :)
            ax.plot(dates, cash, linewidth=1, alpha=0.2, color='b')

    # format the ticks
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(month_fmt)

    # round to nearest years.
    datemin = np.datetime64(dates[0], 'M')
    datemax = np.datetime64(dates[-1], 'M') + np.timedelta64(1, 'M')
    ax.set_xlim(datemin, datemax)

    # format the coords message box
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = lambda x: '$%1.2f' % x  # format the price.
    ax.grid(True)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()

    formatter = ticker.FuncFormatter(lambda x, p: '£' + format(int(x), ','))
    ax.yaxis.set_major_formatter(formatter)

    ax.yaxis.set_major_locator(ticker.MultipleLocator(25000))

    plt.ylabel('Cash at bank')
    plt.xlabel('Date')
    plt.title('Simulation')
    plt.show()


def run_model(
        *,
        model,
        dates: pd.date_range,
        iterations: int=20
):

    all_results = [model(dates=dates) for x in range(iterations)]

    all_cash_series = []

    for result in all_results:

        def get_cash_at_bank(result: list):
            cash_at_bank = None
            for s in result:
                if cash_at_bank is not None:
                    cash_at_bank += s.cumsum()
                else:
                    cash_at_bank = s.cumsum()
            return cash_at_bank

        all_cash_series.append(get_cash_at_bank(result))

    plot_cash_series(all_cash_series, dates)
