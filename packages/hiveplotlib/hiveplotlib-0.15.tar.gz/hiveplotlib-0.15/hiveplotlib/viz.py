# Gary Koplik
# gary<dot>koplik<at>geomdata<dot>com
# August, 2020
# viz.py

"""
Viz functions to be called on `hiveplotlib.HivePlot` instances.
"""

import matplotlib.pyplot as plt
import numpy as np
from hiveplotlib.utils import polar2cartesian
import warnings


def axes_viz_mpl(hive_plot: "HivePlot instance",
                 fig: "matplotlib figure" or None = None, ax: "matplotlib axis" or None = None,
                 figsize: tuple = (10, 10), center_plot: bool = True, buffer: float = 0.1,
                 show_axes_labels: bool = True, axes_labels_buffer: float = 1.1,
                 axes_labels_fontsize: int = 16, mpl_axes_off: bool = True, **axes_kwargs):
    """
    ``matplotlib`` visualization of axes in a ``HivePlot`` instance.

    :param hive_plot: ``HivePlot`` instance for which we want to draw edges.
    :param fig: default ``None`` builds new figure. If a figure is specified, ``Axis`` instances will be
        drawn on that figure. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param ax: default ``None`` builds new axis. If an axis is specified, ``Axis`` instances will be drawn on that
        figure. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param figsize: size of figure. Note: only works if instantiating new figure and axes (e.g. ``fig`` and ``ax`` are
        ``None``).
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that ``Axis`` instances
        can be drawn around.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g setting ``buffer`` to 0.1 will find
        the maximum radius spanned by an ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``.
    :param show_axes_labels: whether to label the hive plot axes in the figure (uses ``Axis.long_name`` for each
        ``Axis``.)
    :param axes_labels_buffer: fraction which to radially buffer axes labels (e.g. setting ``axes_label_buffer`` to 1.1
        will be 10% further past the end of the axis moving from the origin of the plot).
    :param axes_labels_fontsize: font size for hive plot axes labels.
    :param mpl_axes_off: whether to turn off Cartesian x, y axes in resulting ``matplotlib`` figure (default ``True``
        hides the x and y axes).
    :param axes_kwargs: additional params that will be applied to all hive plot axes. Note,these are kwargs that affect
        a ``plt.plot()`` call.
    :return: ``matplotlib`` figure, axis.
    """

    # allow for plotting onto specified figure, axis
    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    # some default kwargs for the axes
    if 'c' not in axes_kwargs:
        axes_kwargs['c'] = 'black'
    if 'alpha' not in axes_kwargs:
        axes_kwargs['alpha'] = 0.5

    for axis in hive_plot.axes.values():
        to_plot = np.vstack((axis.start, axis.end))
        ax.plot(to_plot[:, 0], to_plot[:, 1], **axes_kwargs)
        if center_plot:
            plt.axis("equal")
            # center plot at (0, 0)
            max_radius = max([axis.polar_end for axis in hive_plot.axes.values()])
            # throw in a minor buffer
            buffer_radius = buffer * max_radius
            max_radius += buffer_radius

            ax.set_xlim(-max_radius, max_radius)
            ax.set_ylim(-max_radius, max_radius)

        if show_axes_labels:
            # place labels just beyond end of axes radially outward
            x, y = polar2cartesian(axes_labels_buffer * axis.polar_end, axis.angle)
            ax.text(x, y, axis.long_name, fontsize=axes_labels_fontsize)
    if mpl_axes_off:
        ax.axis("off")

    return fig, ax


def node_viz_mpl(hive_plot: "HivePlot instance",
                 fig: "matplotlib figure" or None = None, ax: "matplotlib axis" or None = None,
                 figsize: tuple = (10, 10), center_plot: bool = True, buffer: float = 0.1,
                 mpl_axes_off: bool = True, **scatter_kwargs):
    """
    ``matplotlib`` visualization of nodes in a ``HivePlot`` instance that have been placed on its axes.

    :param hive_plot: ``HivePlot`` instance for which we want to draw edges.
    :param fig: default ``None`` builds new figure. If a figure is specified, ``Axis`` instances will be
        drawn on that figure. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param ax: default ``None`` builds new axis. If an axis is specified, ``Axis`` instances will be drawn on that
        figure. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param figsize: size of figure. Note: only works if instantiating new figure and axes (e.g. ``fig`` and ``ax`` are
        ``None``).
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that ``Axis`` instances
        can be drawn around.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g setting ``buffer`` to 0.1 will find
        the maximum radius spanned by an ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``.
    :param mpl_axes_off: whether to turn off Cartesian x, y axes in resulting ``matplotlib`` figure (default ``True``
        hides the x and y axes).
    :param scatter_kwargs: additional params that will be applied to all hive plot nodes. Note, these are kwargs that
        affect a ``plt.scatter()`` call.
    :return: ``matplotlib`` figure, axis.
    """

    # allow for plotting onto specified figure, axis
    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    # some default kwargs for the axes
    if 'c' not in scatter_kwargs:
        scatter_kwargs['c'] = 'black'
    if 'alpha' not in scatter_kwargs:
        scatter_kwargs['alpha'] = 0.8
    if 's' not in scatter_kwargs:
        scatter_kwargs["s"] = 20

    for axis in hive_plot.axes.values():
        to_plot = axis.node_placements.values[:, :2]
        if to_plot.shape[0] > 0:
            ax.scatter(to_plot[:, 0], to_plot[:, 1], **scatter_kwargs)
        else:
            warnings.warn(
                "At least one of your axes has no nodes placed on it yet. " +
                "Nodes can be placed on axes by running `HivePlot.place_nodes_on_axis()`",
                stacklevel=2)
        if center_plot:
            plt.axis("equal")
            # center plot at (0, 0)
            max_radius = max([a.polar_end for a in hive_plot.axes.values()])
            # throw in a minor buffer
            buffer_radius = buffer * max_radius
            max_radius += buffer_radius

            ax.set_xlim(-max_radius, max_radius)
            ax.set_ylim(-max_radius, max_radius)
    if mpl_axes_off:
        ax.axis("off")

    return fig, ax


def edge_viz_mpl(hive_plot: "HivePlot instance",
                 fig: "matplotlib figure" or None = None, ax: "matplotlib axis" or None = None,
                 figsize: tuple = (10, 10), mpl_axes_off: bool = True, **edge_kwargs):
    """
    ``matplotlib`` visualization of constructed edges in a ``HivePlot`` instance.

    :param hive_plot: ``HivePlot`` instance for which we want to draw edges.
    :param fig: default ``None`` builds new figure. If a figure is specified, ``Axis`` instances will be
        drawn on that figure. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param ax: default ``None`` builds new axis. If an axis is specified, ``Axis`` instances will be drawn on that
        figure. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param figsize: size of figure. Note: only works if instantiating new figure and axes (e.g. ``fig`` and ``ax`` are
        ``None``).
    :param mpl_axes_off: whether to turn off Cartesian x, y axes in resulting ``matplotlib`` figure (default ``True``
        hides the x and y axes).
    :param edge_kwargs: additional params that will be applied to all edges on all axes (but kwargs specified beforehand
        in ``HivePlot.connect_axes()`` or ``HivePlot.add_edge_kwargs()`` will take priority).
        To overwrite previously set kwargs, see ``HivePlot.add_edge_kwargs()`` for more. Note, these are kwargs that
        affect a ``plt.plot()`` call.
    :return: `matplotlib` figure, axis.
    """

    # make sure edges have already been created
    if len(list(hive_plot.edges.keys())) == 0:
        warnings.warn(
            "Your hive plot does not have any specified edges yet. " +
            "Edges can be created for plotting by running `HivePlot.connect_axes()`",
            stacklevel=2)

    # allow for plotting onto specified figure, axis
    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    for a0 in hive_plot.edges.keys():
        for a1 in hive_plot.edges[a0].keys():
            for tag in hive_plot.edges[a0][a1].keys():
                temp_edge_kwargs = edge_kwargs.copy()

                # only run plotting of edges that exist
                if "curves" in hive_plot.edges[a0][a1][tag]:

                    # create edge_kwargs key if needed
                    if "edge_kwargs" not in hive_plot.edges[a0][a1][tag]:
                        hive_plot.edges[a0][a1][tag]["edge_kwargs"] = dict()

                    # don't use kwargs specified in this function call if already specified
                    for k in list(temp_edge_kwargs.keys()):
                        if k in hive_plot.edges[a0][a1][tag]["edge_kwargs"]:
                            warnings.warn(f"Specified kwarg {k} but already set as kwarg for edge tag {tag} "
                                          f"going from edges {a0} to {a1}. Preserving kwargs already set.\n"
                                          "(These kwargs can be changed using the `add_edge_kwargs()` method "
                                          "for your `HivePlot` instance)", stacklevel=2)
                            del temp_edge_kwargs[k]

                    # some default kwargs for the axes if not specified anywhere
                    if 'c' not in hive_plot.edges[a0][a1][tag]["edge_kwargs"] and 'c' not in temp_edge_kwargs:
                        temp_edge_kwargs['c'] = 'black'
                    if 'alpha' not in hive_plot.edges[a0][a1][tag]["edge_kwargs"] and 'alpha' not in temp_edge_kwargs:
                        temp_edge_kwargs['alpha'] = 0.5

                    # grab the requested array of discretized curves
                    edge_arr = hive_plot.edges[a0][a1][tag]["curves"]
                    ax.plot(edge_arr[:, 0], edge_arr[:, 1],
                            **hive_plot.edges[a0][a1][tag]["edge_kwargs"], **temp_edge_kwargs)

    if mpl_axes_off:
        ax.axis("off")

    return fig, ax


def hive_plot_viz_mpl(hive_plot: "HivePlot instance",
                      fig: "matplotlib figure" or None = None, ax: "matplotlib axis" or None = None,
                      figsize: tuple = (10, 10), center_plot: bool = True, buffer: float = 0.1,
                      show_axes_labels: bool = True, axes_labels_buffer: float = 1.1,
                      axes_labels_fontsize: int = 16, mpl_axes_off: bool = True, **edge_kwargs):
    """
    Default ``matplotlib`` visualization of a ``HivePlot`` instance.

    :param hive_plot: ``HivePlot`` instance for which we want to draw edges
    :param fig: default ``None`` builds new figure. If a figure is specified, ``Axis`` instances will be
        drawn on that figure. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param ax: default ``None`` builds new axis. If an axis is specified, ``Axis`` instances will be drawn on that
        figure. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param figsize: size of figure. Note: only works if instantiating new figure and axes (e.g. ``fig`` and ``ax`` are
        ``None``).
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that ``Axis`` instances
        can be drawn around.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g setting ``buffer`` to 0.1 will find
        the maximum radius spanned by an ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``.
    :param show_axes_labels: whether to label the hive plot axes in the figure (uses ``Axis.long_name`` for each
        ``Axis``.)
    :param axes_labels_buffer: fraction which to radially buffer axes labels (e.g. setting ``axes_label_buffer`` to 1.1
        will be 10% further past the end of the axis moving from the origin of the plot).
    :param axes_labels_fontsize: font size for hive plot axes labels.
    :param mpl_axes_off: whether to turn off Cartesian x, y axes in resulting ``matplotlib`` figure (default ``True``
        hides the x and y axes).
    :param edge_kwargs: additional params that will be applied to all edges on all axes (but kwargs specified beforehand
        in ``HivePlot.connect_axes()`` or ``HivePlot.add_edge_kwargs()`` will take priority).
        To overwrite previously set kwargs, see ``HivePlot.add_edge_kwargs()`` for more. Note, these are kwargs that
        affect a ``plt.plot()`` call.
    :return: ``matplotlib`` figure, axis.
    """

    fig, ax = axes_viz_mpl(hive_plot=hive_plot, fig=fig, ax=ax, figsize=figsize, center_plot=center_plot,
                           buffer=buffer, show_axes_labels=show_axes_labels, axes_labels_buffer=axes_labels_buffer,
                           axes_labels_fontsize=axes_labels_fontsize, mpl_axes_off=mpl_axes_off)
    node_viz_mpl(hive_plot=hive_plot, fig=fig, ax=ax)
    edge_viz_mpl(hive_plot=hive_plot, fig=fig, ax=ax, zorder=-1, **edge_kwargs)

    return fig, ax
