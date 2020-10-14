import matplotlib.pyplot as plt
import matplotlib as mpl
import powerlaw

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def create_plot(path_to_save: str, title: str, xlabel: str, xdata: list, ylabel: str, ydata: list, yticks: list = None,
                also_log_scale: bool = False, log_yticks: list = None, powerlaw_xmin=None, powerlaw_xmax=None):
    fig = plt.figure()
    fig.set_size_inches(14.0, 14.0)

    # Plot in linear scale
    ax = plt.subplot(2 if also_log_scale else 1, 1, 1)
    plt.scatter(xdata, ydata)
    plt.title(title + ' (linear scale)' if also_log_scale else '')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if yticks:
        ax.set_ylim(ymin=yticks[0], ymax=yticks[len(yticks) - 1])
        ax.set_yticks(yticks)
    plt.grid()

    # Plot in log scale
    if also_log_scale:
        ax = plt.subplot(2, 1, 2)
        plt.scatter(xdata, ydata)
        plt.title(title + ' (log scale)')
        plt.xlabel('log(' + xlabel + ')')
        plt.ylabel('log(' + ylabel + ')')
        ax.set_xscale('log')
        ax.set_yscale('log')
        if log_yticks:
            ax.set_ylim(ymin=log_yticks[0], ymax=log_yticks[len(log_yticks)-1])
            ax.set_yticks(log_yticks)
        ax.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
        plt.grid()

    # Plot power law
    if powerlaw_xmin and powerlaw_xmax:
        fit = powerlaw.Fit(xdata + 1, xmin=powerlaw_xmin, xmax=powerlaw_xmax, discrete=True)
    else:
        fit = powerlaw.Fit(xdata + 1, discrete=True)

    fit.power_law.plot_pdf(color='r', linestyle='--', label='fit pdf')

    fig.savefig(path_to_save)

    if also_log_scale:
        return fit.power_law.alpha
    return

