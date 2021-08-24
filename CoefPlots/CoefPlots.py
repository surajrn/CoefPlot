import numpy as np
import seaborn as sns



import matplotlib.pyplot as plt
import matplotlib as mpl


mpl.rc('xtick', labelsize=11)
mpl.rc('ytick', labelsize=11)
mpl.rcParams["savefig.dpi"]     = 300
# matplotlib.rc('text', usetex=True)
from collections import namedtuple, defaultdict


#Create default settings for the coefficient plot
Settings=namedtuple('Settings', ["figwidth", "table_position", "fontsize",
                                 "marker_props", "errorbar_props","vline_props"])


defaultSettings=Settings(
    figwidth=8,
    table_position='left',
    fontsize=11,
    marker_props={"fmt":"rd", "markersize":4},
    errorbar_props={"linestyle":"", "linewidth":1, "color":"black", "capsize":4},
    vline_props={"linestyle":"--", "color":"grey", "linewidth":0.5}
)


# newSettings=Settings(
#     figwidth=8,
#     table_position='left',
#     fontsize=11,
#     marker={"fmt":"rd", "markersize":4},
#     errorbar={"linestyle":"", "linewidth":1, "color":"black", "capsize":4},
#     vline={"linestyle":"--", "color":"grey", "linewidth":0.5}
# )


def rebuild_font_cache():
    import matplotlib.font_manager
    matplotlib.font_manager._rebuild()


def adjust_panel(ax):
    """
    Get the length of the longest label
    """

    plt.draw()
    yax=ax.get_yaxis()
#     ylabs=ax.get_yticklabels()

    pad = max([T.label.get_window_extent().width for T in yax.majorTicks])

    return pad

def set_labels(ax, columns, y, table_position):
    """
    Set the table either on the left or right.
    """
    if table_position=='left':
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        bbox=(-max(0.125*len(columns),0.3), 0,  max(0.125*len(columns),0.3), (len(y)+1)/len(y))
    else:
        bbox=(1, 0,  max(0.125*len(columns),0.3), (len(y)+1)/len(y))

    return bbox

def plot_axplot(ax, x, y, **kwargs):
    """
    Add scatter plot to axis
    """
    if "fmt" in kwargs.keys():
        fmt=kwargs["fmt"]
        del kwargs["fmt"]
    else:
        fmt=settings.marker_props["fmt"]


    kwargs["markersize"] = kwargs.get("markersize", settings.marker_props["markersize"])
    ax.plot(x, y, fmt, **kwargs)


def plot_errorbar(ax, x, y, xerror,**kwargs):
    """
    Add errorbars to axis
    """
    kwargs["linestyle"]=kwargs.get("linestyle", settings.errorbar_props["linestyle"])
    kwargs["linewidth"]=kwargs.get("linewidth", settings.errorbar_props["linewidth"])
    kwargs["color"]=kwargs.get("color", settings.errorbar_props["color"])
    kwargs["capsize"]=kwargs.get("capsize", settings.errorbar_props["capsize"])

    ax.errorbar(x=x, y=y, xerr=xerror, **kwargs)

def plot_axvline(ax, **kwargs):
    """
    Add vertical line to axis
    """

    kwargs["linestyle"]=kwargs.get("linestyle", settings.vline_props["linestyle"])
    kwargs["linewidth"]=kwargs.get("linewidth", settings.vline_props["linewidth"])
    kwargs["color"]=kwargs.get("color", settings.vline_props["color"])

    ax.axvline(x=0, **kwargs)


def format_axes(ax, y, ylabels, **kwargs):
    """
    General axis formatting
    """

    kwargs["fontsize"]=kwargs.get("fontsize", settings.fontsize)
    kwargs["ha"]=kwargs.get("ha", "left")

    ax.set_ylim(0,len(ylabels) )
    ax.set_yticks(y)
    ax.set_yticklabels(ylabels, **kwargs)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(left=False, right=False)

def make_table(ax, tabledata, columns, col_labels, bbox):
    """
    Add table to axis.
    Table location is determined by the table position setting in Settings()
    """
    y=tabledata.shape[0]
    colWidths=[0.02]*len(columns)

    the_table = ax.table(cellText=tabledata,
                              # rowColours=colors,
                              colWidths=colWidths,
                              colLabels=col_labels,
                              cellLoc='center',
                              colLoc='center',
                             bbox=bbox)

    cellDict = the_table.properties()["celld"]

    for i in range(0, len(columns)):
        cellDict[(0,i)].visible_edges='B'

    for row in range(1, y+1):
        for col in range(0, len(columns)):
            cellDict[(row, col)].visible_edges=''


    the_table.auto_set_font_size(False)
    the_table.set_fontsize(settings.fontsize)





def make_coef_plot(ylabels:list,
                   x:list,
                   xerror:list,
                   tabledata:np.ndarray,
                   table_coldict:dict,
                   table_position="right",
                   kwarg_dict={}):

    """
    Function to make coefficient plots with table.

    Parameters:
    ylabels: list of y axis labels
    x: list of coefficient values
    xerror: list of confidence interval "lengths"
    tabledata: np.ndarray containing data for the table
    table_coldict: dictionary containing column variables and column names for the table
    kwarg_dict: dictionary (optional) -- allows additional formatting of various plot elements.
                Specify dictionary using the following keywords:
                "marker_kwargs": formatting for the markers
                "errorbar_kwargs":formatting for the errorbars
                "axvline_kwargs": formatting for the vertical line at 0
                "ylabel_kwargs": general formatting for y axis labels

    Example function call:

    make_coef_plot(ylabels,
               x,
               xerror,
               tabledata,
               col_dict,
               table_position='left',
              kwarg_dict={"marker_kwargs":{"fmt":"bs"}})
    """


    for kdict in ["marker_kwargs", "errorbar_kwargs",
                 "axvline_kwargs","ylabel_kwargs"]:
        kwarg_dict[kdict]=kwarg_dict.setdefault(kdict, {})

    fig, ax=plt.subplots(figsize=(settings.figwidth,len(ylabels)/2))



    y=np.arange(0.5, len(ylabels), 1)

    pads=[]
    columns=table_coldict.keys()
    col_labels=list(table_coldict.values())

    bbox=set_labels(ax, columns, y, table_position)

    plot_axplot(ax, x, y, **kwarg_dict["marker_kwargs"])
    plot_errorbar(ax, x, y, xerror, **kwarg_dict["errorbar_kwargs"])
    plot_axvline(ax, **kwarg_dict["axvline_kwargs"])
    format_axes(ax, y, ylabels, **kwarg_dict["ylabel_kwargs"])

    make_table(ax, tabledata, columns, col_labels, bbox)



    #Padding
    pad=adjust_panel(ax)
    pads.append(pad)
    plt.draw()
    yax=ax.get_yaxis()
    yax.set_tick_params(pad=min(pads)+10)

    # plt.tight_layout()



    plt.show()
    return fig


settings=defaultSettings
rebuild_font_cache()
