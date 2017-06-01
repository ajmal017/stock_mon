import tushare as ts

import matplotlib.pyplot as plt
from matplotlib.finance import quotes_historical_yahoo_ochl
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY,date2num
import datetime
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.font_manager import FontProperties

#df = ts.get_k_data('603869')
#print(df)

#ticker = '603869.ss'
#date1 = datetime.date( 2015, 7, 10 )
#date2 = datetime.date( 2016, 7, 10 )

#quotes = quotes_historical_yahoo_ochl(ticker, date1, date2)

#print(quotes)

def _candlestick(ax, df, width=0.2, colorup='k', colordown='r',
                 alpha=1.0):

    """
    Plot the time, open, high, low, close as a vertical line ranging
    from low to high.  Use a rectangular bar to represent the
    open-close span.  If close >= open, use colorup to color the bar,
    otherwise use colordown

    Parameters
    ----------
    ax : `Axes`
        an Axes instance to plot to
    df : pandas data from tushare
    width : float
        fraction of a day for the rectangle width
    colorup : color
        the color of the rectangle where close >= open
    colordown : color
         the color of the rectangle where close <  open
    alpha : float
        the rectangle alpha level
    ochl: bool
        argument to select between ochl and ohlc ordering of quotes

    Returns
    -------
    ret : tuple
        returns (lines, patches) where lines is a list of lines
        added and patches is a list of the rectangle patches added

    """

    OFFSET = width / 2.0

    lines = []
    patches = []
    for date_string,row in df.iterrows():
        date_time = datetime.datetime.strptime(date_string,'%Y-%m-%d')
        t = date2num(date_time)
        open, high, close, low = row[:4]

        if close >= open:
            color = colorup
            lower = open
            height = close - open
        else:
            color = colordown
            lower = close
            height = open - close

        vline = Line2D(
            xdata=(t, t), ydata=(low, high),
            color=color,
            linewidth=0.5,
            antialiased=True,
        )

        rect = Rectangle(
            xy=(t - OFFSET, lower),
            width=width,
            height=height,
            facecolor=color,
            edgecolor=color,
        )
        rect.set_alpha(alpha)

        lines.append(vline)
        patches.append(rect)
        ax.add_line(vline)
        ax.add_patch(rect)
    ax.autoscale_view()

    return lines, patches

def draw_k_pic(df, code, name):
    mondays = WeekdayLocator(MONDAY)            # 主要刻度
    alldays = DayLocator()                      # 次要刻度
    #weekFormatter = DateFormatter('%b %d')     # 如：Jan 12
    mondayFormatter = DateFormatter('%m-%d-%Y') # 如：2-29-2015
    dayFormatter = DateFormatter('%d')          # 如：12
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(mondayFormatter)

    _candlestick(ax, df, width=0.6, colorup='r', colordown='g')

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')


    ax.grid(True)
    plt.title(name + '  ' + code, fontproperties=zhfont)
    plt.show()

#df = ts.get_k_data('603869')
if __name__ == "__main__":
    zhfont = FontProperties(fname='/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc')
    df = ts.get_hist_data('603869', start='2016-10-07', end='2016-12-07')
    df = df.sort_index(0)
    draw_k_pic(df, '603869', '北部湾旅')
