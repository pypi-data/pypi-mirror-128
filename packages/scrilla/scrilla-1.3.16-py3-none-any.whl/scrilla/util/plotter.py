import os
import datetime
from typing import List, Union
import numpy
import matplotlib
from PIL import Image

from matplotlib.figure import Figure
from matplotlib import dates as mdates
from matplotlib.ticker import PercentFormatter

from scrilla import settings
from scrilla.static import formats, keys
from scrilla.analysis.objects.portfolio import Portfolio
from scrilla.analysis.objects.cashflow import Cashflow
from scrilla.errors import InputValidationError
from scrilla.util import dater

APP_ENV = os.environ.setdefault('APP_ENV', 'local')

if APP_ENV == 'local':
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    matplotlib.use("Qt5Agg")
elif APP_ENV == 'container':
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    matplotlib.use("agg")


def _show_or_save(canvas: FigureCanvas, show: bool = True, savefile: str = None) -> Union[FigureCanvas, None]:
    if savefile is not None:
        canvas.print_jpeg(filename_or_obj=savefile)

    s, (width, height) = canvas.print_to_buffer()
    im = Image.frombytes("RGBA", (width, height), s)

    if show:
        im.show()
        return None
    canvas.draw()
    return canvas


def plot_qq_series(ticker: str, qq_series: list, show: bool = True, savefile: str = None) -> Union[FigureCanvas, None]:
    title = f'{ticker} Return Q-Q Plot'
    normal_series = []
    sample_series = []
    for point in qq_series:
        normal_series.append(point[0])
        sample_series.append(point[1])

    canvas = FigureCanvas(Figure())
    axes = canvas.figure.subplots()

    axes.plot(normal_series, sample_series,
              linestyle="None", marker=".", markersize=10.0)
    # axes.plot(normal_series, normal_series)
    axes.grid()
    axes.set_xlabel('Normal Percentiles')
    axes.set_ylabel('Sample Percentiles')
    axes.set_title(title)

    return _show_or_save(canvas=canvas, show=show, savefile=savefile)


def plot_correlation_series(tickers: list, series: dict, show: bool = True, savefile: str = None) -> Union[FigureCanvas, None]:
    start, end = list(series.keys())[-1], list(series.keys())[0]
    title = f'({tickers[0]}, {tickers[1]}) correlation time series'
    subtitle = f'{start} to {end}, rolling {settings.DEFAULT_ANALYSIS_PERIOD}-day estimate'

    canvas = FigureCanvas(Figure())
    figure = canvas.figure
    axes = figure.subplots()

    locator = mdates.AutoDateLocator()
    formatter = mdates.AutoDateFormatter(locator)

    correl_history, dates = [], []
    for date in series:
        dates.append(dater.parse_date_string(date))
        correl_history.append(series[date])

    axes.plot(dates, correl_history)
    axes.grid()
    axes.xaxis.set_major_locator(locator)
    axes.xaxis.set_major_formatter(formatter)
    axes.set_ylabel('Correlation')
    axes.set_xlabel('Dates')
    axes.set_title(subtitle, fontsize=12)
    figure.suptitle(title, fontsize=18)
    figure.autofmt_xdate()

    return _show_or_save(canvas=canvas, show=show, savefile=savefile)


def plot_frontier(portfolio: Portfolio, frontier: list, show: bool = True, savefile: str = None) -> Union[FigureCanvas, None]:
    title = " ("
    for i, item in enumerate(portfolio.tickers):
        if i != (len(portfolio.tickers) - 1):
            title += item + ", "
        else:
            title += item + ") Efficient Frontier"

    return_profile, risk_profile = [], []
    for allocation in frontier:
        return_profile.append(portfolio.return_function(allocation))
        risk_profile.append(portfolio.volatility_function(allocation))

    canvas = FigureCanvas(Figure())
    axes = canvas.figure.subplots()

    axes.plot(risk_profile, return_profile, linestyle='dashed')
    axes.grid()
    axes.set_xlabel('Volatility')
    axes.set_ylabel('Return')
    axes.set_title(title)

    return _show_or_save(canvas=canvas, show=show, savefile=savefile)


def plot_yield_curve(yield_curve: dict, show: bool = True, savefile: str = None) -> Union[FigureCanvas, None]:
    title = f'US Treasury Yield Curve On {list(yield_curve.keys())[0]}'

    canvas = FigureCanvas(Figure())
    axes = canvas.figure.subplots()

    maturities, rates = [], yield_curve[list(yield_curve.keys())[0]]
    yield_map = keys.keys['SERVICES']['STATISTICS']['QUANDL']['MAP']['YIELD_CURVE']
    for i in range(len(rates)):
        maturities.append(yield_map[keys.keys['YIELD_CURVE'][i]])

    axes.plot(maturities, rates, linestyle="dashed",
              marker=".", markersize=10.0)
    axes.grid()
    axes.set_xlabel('Maturity')
    axes.set_ylabel('Annual Yield %')
    axes.set_title(title)

    return _show_or_save(canvas=canvas, show=show, savefile=savefile)


def plot_return_histogram(ticker: str, sample: list, show: bool = True, savefile: str = None) -> Union[FigureCanvas, None]:
    canvas = FigureCanvas(Figure())
    axes = canvas.figure.subplots()

    axes.hist(x=sample, bins=formats.formats['BINS'], density=True)
    axes.xaxis.set_major_formatter(PercentFormatter(xmax=1))
    axes.set_title(f'Distribution of {ticker} Returns')
    axes.set_xlabel('Daily Return')

    return _show_or_save(canvas=canvas, show=show, savefile=savefile)


def plot_profiles(symbols: list, profiles: dict, show: bool = True, savefile: str = None, subtitle: str = None) -> Union[FigureCanvas, None]:
    canvas = FigureCanvas(Figure())

    no_symbols = len(symbols)
    axes = canvas.figure.subplots()

    title = "("
    for symbol in symbols:
        if symbols.index(symbol) != (len(symbols)-1):
            title += symbol + ", "
        else:
            title += symbol + ') Risk-Return Profile'
            if subtitle is not None:
                title += "\n" + subtitle

    return_profile, risk_profile = [], []
    for profile in profiles:
        return_profile.append(profiles[profile]['annual_return'])
        risk_profile.append(profiles[profile]['annual_volatility'])

    axes.plot(risk_profile, return_profile,
              linestyle='None', marker=".", markersize=10.0)
    axes.grid()
    axes.set_xlabel('Volatility')
    axes.set_ylabel('Return')
    axes.set_title(title)

    for i in range(no_symbols):
        axes.annotate(symbols[i], (risk_profile[i], return_profile[i]))

    return _show_or_save(canvas=canvas, show=show, savefile=savefile)

    # TODO: figure out date formatting for x-axis


def plot_moving_averages(symbols: List[str], averages_output: List[List[float]], periods: List[int], show: bool = True, savefile: str = None) -> Union[FigureCanvas, None]:
    averages, dates = averages_output
    canvas = FigureCanvas(Figure())
    axes = canvas.figure.subplots()
    ma1_label, ma2_label, ma3_label = f'MA({periods[0]})', f'MA({periods[1]})', f'MA({periods[2]})'

    if dates is None:
        ma1s, ma2s, ma3s = [], [], []
        for i in range(len(symbols)):
            ma1s.append(averages[i][0])
            ma2s.append(averages[i][1])
            ma3s.append(averages[i][2])

        width = formats.formats['BAR_WIDTH']
        x = numpy.arange(len(symbols))

        axes.bar(x + width, ma1s, width, label=ma1_label)
        axes.bar(x, ma2s, width, label=ma2_label)
        axes.bar(x - width, ma3s, width, label=ma3_label)

        axes.set_ylabel('Annual Logarithmic Return')
        axes.set_title(
            'Moving Averages of Annualized Daily Return Grouped By Equity')
        axes.set_xticks(x)
        axes.set_xticklabels(symbols)
        axes.legend()

    else:

        # TODO: generate different locators based on length of period
        x = [datetime.datetime.strptime(dater.date_to_string(
            date), '%Y-%m-%d').toordinal() for date in dates]
        date_locator = matplotlib.dates.WeekdayLocator(
            byweekday=(matplotlib.dates.WE))
        date_format = matplotlib.dates.DateFormatter('%m-%d')

        for i, item in enumerate(symbols):
            ma1s, ma2s, ma3s = [], [], []
            ma1_label, ma2_label, ma3_label = f'{item}_{ma1_label}', f'{item}_{ma2_label}', f'{item}_{ma3_label}'
            for j in range(len(dates)):
                MA_1 = averages[i][0][j]
                ma1s.append(MA_1)

                MA_2 = averages[i][1][j]
                ma2s.append(MA_2)

                MA_3 = averages[i][2][j]
                ma3s.append(MA_3)

            start_date, end_date = dates[0], dates[-1]
            title_str = f'Moving Averages of Annualized Return From {start_date} to {end_date}'

            axes.plot(x, ma1s, linestyle="solid",
                      color="darkgreen", label=ma1_label)
            axes.plot(x, ma2s, linestyle="dotted",
                      color="gold", label=ma2_label)
            axes.plot(x, ma3s, linestyle="dashdot",
                      color="orangered", label=ma3_label)

        axes.set_title(title_str)
        axes.set_ylabel('Annualized Logarthmic Return')
        axes.set_xlabel('Dates')
        axes.xaxis.set_major_locator(date_locator)
        axes.xaxis.set_major_formatter(date_format)

        axes.legend()

    return _show_or_save(canvas=canvas, show=show, savefile=savefile)


def plot_cashflow(ticker: str, cashflow: Cashflow, show: bool = True, savefile: str = None) -> Union[FigureCanvas, None]:
    if not cashflow.beta or not cashflow.alpha or len(cashflow.sample) < 3:
        raise InputValidationError(
            "Cashflow model does not contain enough information to be plotted")

    canvas = FigureCanvas(Figure())
    figure = canvas.figure
    axes = figure.subplots()

    sup_title_str = f'{ticker} Dividend Linear Regression Model'
    title_str = f'NPV(dividends | discount = {round(cashflow.discount_rate,4)}) = $ {round(cashflow.calculate_net_present_value(), 2)}'

    dividend_history, ordinal_x, dates = [], [], []
    for date in cashflow.sample:
        dates.append(date)
        ordinal_x.append(datetime.datetime.strptime(
            date, '%Y-%m-%d').toordinal())
        dividend_history.append(cashflow.sample[date])

    dates.reverse()

    model_map = list(map(lambda x: cashflow.alpha +
                     cashflow.beta*x, cashflow.time_series))

    axes.scatter(ordinal_x, dividend_history, marker=".")
    axes.plot(ordinal_x, model_map)
    axes.grid()
    # axes.xaxis.set_major_formatter(date_format)
    axes.set_xticklabels(dates)
    axes.set_ylabel('Dividend Amount')
    axes.set_xlabel('Payment Date')
    axes.set_title(title_str, fontsize=12)
    figure.suptitle(sup_title_str, fontsize=18)
    figure.autofmt_xdate()

    return _show_or_save(canvas=canvas, show=show, savefile=savefile)
