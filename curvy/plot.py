import matplotlib.pyplot as plt

def mpl_create_curve_plot(x):
    plt.ioff()
    fig, ax = plt.subplots(figsize=(15,10))
    ax.set_title('Price curve')
    ax.set_ylabel('Price')
    ax.set_xlabel('Date')
    ax.set_xlim(x[0], x[-1])
    ax.grid(True)
    return fig, ax

def mpl_plot_curves(dates, prices, fig, ax, *args):
    ax.plot(dates, prices, color='blue')
    for arg in args:
        date_range, y, color, linestyle = arg
        ax.plot(date_range, y, color=color, linestyle=linestyle)
    plt.show()

def mpl_plot_curve_sections(dates, prices, fig, ax, *args, hide_price=False):
    if not hide_price:
        ax.plot(dates, prices, color='blue')
    for arg in args:
        for i in range(0, len(arg[0])):
            ax.plot(arg[0][i], arg[1][i])
    plt.show()